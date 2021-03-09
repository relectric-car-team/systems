from itertools import count
from json import JSONDecodeError
# demo
from random import randint
from time import sleep

import zmq
from zmq import Socket
from zmq.decorators import socket
from zmq.utils import jsonapi

from .abstract import Client
from .controllers import controllers


class CoreServer:

    def __init__(self, backend_binding: str, frontend_binding: str):
        """Basic ZMQ server for communication between frontend clients and backend workers.

        Args:
            backend_binding (str): Address of backend binding
            frontend_binding (str): Address of frontend binding
        """
        self.backend_binding = backend_binding
        self.frontend_binding = frontend_binding
        self.worker_ids = set()
        self.client_identities = set()

    @socket(zmq.ROUTER)
    @socket(zmq.DEALER)
    def run(self, frontend: Socket, backend: Socket):
        """Start core server to facilitate client to worker communications.

        Args:
            frontend (Socket): @decorator Router socket
            backend (Socket): @decorator Dealer socket
        """
        frontend.bind(self.frontend_binding)
        backend.bind(self.backend_binding)

        poller = zmq.Poller()
        poller.register(backend, zmq.POLLIN)
        poller.register(frontend, zmq.POLLIN)

        print("Server setup finished")

        while (len(self.client_identities) < 2) or (len(self.worker_ids) < 1):
            try:
                pings = dict(poller.poll())
            except KeyboardInterrupt:
                return

            if frontend in pings:
                [client_identity, _] = frontend.recv_multipart()
                self.client_identities.add(client_identity)
                print(f"{client_identity} connected")

            if backend in pings:
                worker_id = backend.recv()
                self.worker_ids.add(worker_id)
                print(f"Worker @ {worker_id} connected")

        backend.send(b'')
        print(f"{len(self.worker_ids)} worker(s) ready")

        for client in self.client_identities:
            frontend.send_multipart([client, b''])
        print(f"Server initialized, connected to {self.client_identities}")

        while True:
            try:
                incoming_messages = dict(poller.poll())
            except KeyboardInterrupt:
                return

            if frontend in incoming_messages:
                message = frontend.recv_multipart()
                backend.send_multipart(message, zmq.NOBLOCK)

            if backend in incoming_messages:
                message = backend.recv_multipart()
                frontend.send_multipart(message)

    def __call__(self):
        return self.run()


class CanbusNet(Client):

    def __init__(self, core_frontend_address: str):
        """Client endpoint for Can Bus communication.

        Args:
            core_frontend_address (str)
        """
        self.core_frontend_address = core_frontend_address
        self.identity = u'canbus'

    @socket(zmq.DEALER)
    def run(self, socket: Socket):
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_frontend_address)
        print(
            f"{self.identity} started, connecting to {self.core_frontend_address}"
        )

        if self.vibe_check_server(socket):
            print(f"{self.identity}: Connection established")
        else:
            print("Connection failure, quitting")
            return

        try:
            while True:
                socket.send_json({"speed": randint(10, 100)})
                message = socket.recv_json()
                print(f"Can Bus received: {message}")
                sleep(1)
        except KeyboardInterrupt:
            return


class PiNet(Client):

    def __init__(self, core_frontend_address: str):
        """Client endpoint for user interface communication.

        # TODO: set up websockets, can be done in ZMQ

        Args:
            core_frontend_address (str)
        """
        self.core_frontend_address = core_frontend_address
        self.identity = u'ui'

    @socket(zmq.DEALER)
    def run(self, socket: Socket):
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_frontend_address)
        print(
            f"{self.identity} started, connecting to {self.core_frontend_address}"
        )

        if self.vibe_check_server(socket):
            print(f"{self.identity}: Connection established")
        else:
            print("Connection failure, quitting")
            return

        try:
            while True:
                socket.send_json({"temperature": randint(15, 25)})
                message = socket.recv()
                print(f"UI received: {message}")
                sleep(2)
        except KeyboardInterrupt:
            return


class ControllerWorker:
    _instance_count = count(0)

    def __init__(self, core_backend_address: str):
        """Prototype worker class, will facilitate controllers.

        Args:
            core_backend_address (str): Core backend binding address
        """
        self._id = next(self._instance_count)
        self.identity = u'controller-worker{}'.format(self._id)
        self.core_backend_address = core_backend_address
        self.controllers = controllers

    @socket(zmq.DEALER)
    def run(self, socket: Socket):
        """Start worker for controller classes.

        Args:
            socket (Socket): @decorator Dealer socket
        """
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_backend_address)
        print(
            f"{self.identity} started, connecting to {self.core_backend_address}"
        )

        socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = socket.recv()
        if b'' in ready_ping:
            print(f"{self.identity}: Connection established")

        while True:
            try:
                identity, message = socket.recv_multipart()
            except KeyboardInterrupt:
                return

            # TODO: fix this try/catch 👇🏽 with a better mechanism
            try:
                message: dict = jsonapi.loads(message)
            except JSONDecodeError:
                continue
            print(f"Worker recieved {message} from {identity}")
            message.update({"processed": True})
            outgoing = jsonapi.dumps(message)
            socket.send_multipart([identity, outgoing])

    def __call__(self) -> None:
        return self.run()
