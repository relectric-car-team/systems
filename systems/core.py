from __future__ import annotations

from itertools import count

import zmq
from loguru import logger
from zmq.utils import jsonapi

from .controllers import controllers


class CoreServer:

    def __init__(self, backend_binding: str, frontend_binding: str):
        """ZMQ server for communication between frontend clients and backend workers.

        Args:
            backend_binding (str): Address of backend binding
            frontend_binding (str): Address of frontend binding
        """
        context = zmq.Context.instance()

        self.backend_binding = backend_binding
        self.frontend_binding = frontend_binding
        self.worker_ids = set()
        self.client_identities = set()

        self.backend = context.socket(zmq.DEALER)
        self.frontend = context.socket(zmq.ROUTER)
        self.poller = zmq.Poller()

    def run(self):
        """Main loop to `run` the server, primarily called through __call__."""
        self.start_listening()
        logger.info("Server listening.")

        while not self.is_fully_connected:
            self.gather_connections()

        self.send_ready_messages()
        logger.info(f"{len(self.worker_ids)} worker(s) ready")
        logger.info(
            f"Server initialized, connected to {self.client_identities}")

        while True:
            self.proxy_messages()

    def start_listening(self):
        """Configure frontend-backend poller and start listening."""
        self.frontend.bind(self.frontend_binding)
        self.backend.bind(self.backend_binding)
        self.poller.register(self.backend, zmq.POLLIN)
        self.poller.register(self.frontend, zmq.POLLIN)

    @property
    def is_fully_connected(self) -> bool:
        """Check if all required clients and workers are connected.

        Returns:
            bool
        """
        # it might be good to parametrize this later on.
        return len(self.client_identities) >= 2 and len(self.worker_ids) >= 1

    def proxy_messages(self):
        """Proxy messages between frontend and backend.

        Currently sending all messages from frontend to backend, all
        messages from backend to frontend. In the future, this is probably
        where the logic for returning message to sender will go.
        """
        incoming_messages = dict(self.poller.poll())

        if self.frontend in incoming_messages:
            message = self.frontend.recv_multipart()
            self.backend.send_multipart(message, zmq.NOBLOCK)

        if self.backend in incoming_messages:
            message = self.backend.recv_multipart()
            self.frontend.send_multipart(message)

    def gather_connections(self):
        """Synchronize start between server and connected sockets."""
        new_connections = dict(self.poller.poll())

        if self.frontend in new_connections:
            [client_identity, _] = self.frontend.recv_multipart()
            self.client_identities.add(client_identity)
            logger.success(f"{client_identity} connected")

        if self.backend in new_connections:
            worker_id = self.backend.recv()
            self.worker_ids.add(worker_id)
            logger.success(f"Worker @ {worker_id} connected")

    def send_ready_messages(self, ready_message: str = b'ready'):
        """Alert frontend and backend connections server is ready to receive.

        Args:
            ready_message (str, optional): Defaults to b''.
        """
        self.backend.send(ready_message)
        for client in self.client_identities:
            self.frontend.send_multipart([client, ready_message])

    def __call__(self) -> None:
        """Handles graceful exiting and sugar for Thread() syntax.

        ::

            server = CoreServer()
            server() # == server.run()
            Thread(target=server) # == Thread(target=server.run)
        ::
        """
        try:
            self.run()
        except KeyboardInterrupt:
            pass

        self.backend.close()
        self.frontend.close()


class BrowserProxy:

    def __init__(self, core_frontend_address: str, websocket_address: str):
        """Transport bridge proxy for communication with broswer.

        Args:
            core_frontend_address (str): Address of frontend connection
            websocket_address (str): Address of websocket binding
        """
        context = zmq.Context.instance()

        self.identity = u'browser'

        self.core_frontend_address = core_frontend_address
        self.websocket_address = websocket_address

        self.browser_socket = context.socket(zmq.DEALER)
        self.browser_socket.identity = self.identity.encode('ascii')
        self.core_socket = context.socket(zmq.DEALER)
        self.core_socket.identity = self.identity.encode('ascii')

    def run(self):
        self.browser_socket.bind(self.websocket_address)
        self.core_socket.connect(self.core_frontend_address)
        zmq.proxy(self.browser_socket, self.core_socket)

    def __call__(self) -> None:
        """Handles graceful exiting and sugar for Thread() syntax."""
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        self.core_socket.close()
        self.browser_socket.close()


class ControllerWorker:
    _instance_count = count(0)

    def __init__(self, core_backend_address: str):
        """Controller worker class to process messages and manipulate controllers.

        Args:
            core_backend_address (str): Core backend binding address.
        """
        context = zmq.Context.instance()
        self._id = next(self._instance_count)
        self.identity = u'controller-worker{}'.format(self._id)
        self.core_backend_address = core_backend_address
        self.controllers = controllers
        # NOTE: we need to look into if we can replace dealer with rep
        self.socket = context.socket(zmq.DEALER)
        self.socket.identity = self.identity.encode('ascii')

    def run(self):
        """Start worker for controller classes."""
        if not self.connect_to_server():
            logger.info(f"{self.identity} quitting")
            return

        while True:
            self.receive_messages()

    def connect_to_server(self) -> bool:
        """Connect and register to server.

        Returns:
            bool: True if connected.
        """
        self.socket.connect(self.core_backend_address)
        logger.info(
            f"{self.identity} started, connecting to {self.core_backend_address}"
        )

        if self.register_to_server():
            logger.success(f"{self.identity}: Connection established")
            return True
        else:
            logger.error("Worker: Connection failure")
            return False

    def receive_messages(self):
        """Loop to listen for and respond to incoming messages."""
        identity, message = self.socket.recv_multipart()
        message: dict = jsonapi.loads(message)
        logger.debug(f"Worker recieved {message} from {identity}")
        self.process_messages(message)
        outgoing = jsonapi.dumps(message)
        self.socket.send_multipart([identity, outgoing])

    def register_to_server(self, ready_message: bytes = b'ready'):
        """Register self to server for synchronized start.

        Args:
            ready_message (bytes, optional): Defaults to b'ready'

        Returns:
            bool: True if connection granted.
        """
        self.socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = self.socket.recv()
        return ready_message in ready_ping

    def process_messages(self, message: list[dict] | dict):
        """Intermediate step for message processing for list vs single element.

        Args:
            message (list[dict] | dict)
        """
        if isinstance(message, list):
            for msg in message:
                self.process_message(msg)
                msg.update({'processed': True})
        else:
            self.process_message(message)
            message.update({'processed': True})

    def process_message(self, message: dict):
        """Process incoming message and update controller.

        Args:
            message (dict)
        """
        controller_name: str = message['controller']

        for attribute, value in message['data'].items():
            old_value = self.controllers[controller_name][attribute]
            self.controllers[controller_name][attribute] = value
            logger.debug(
                f"{controller_name} controller attribute {attribute} changed to "
                f"{value} from {old_value}")

    def __call__(self) -> None:
        """Handles graceful exiting and sugar for Thread() syntax."""
        try:
            self.run()
        except KeyboardInterrupt:
            pass

        self.socket.close()
