from abc import ABC, abstractmethod
from random import randint
from time import sleep

import zmq


class Client(ABC):
    core_frontend_address: str
    identity: str
    socket: zmq.Socket
    is_connected = False

    @abstractmethod
    def run(self) -> None:
        """Start main routine for ZMQ client endpoint.

        Mainly done through __call__().
        """
        pass    # TODO: set up retry system

    def register_to_server(self, ready_message: bytes = b'ready') -> bool:
        """Vibe check server for synchronized start.

        Args:
            ready_message (bytes, optional): Defaults to b'ready'.

        Returns:
            bool: True if connection granted
        """
        self.socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = self.socket.recv()
        return ready_message in ready_ping

    @abstractmethod
    def connect_to_server(self) -> bool:
        """Connect and register to server.

        Returns:
            bool: True if connection successful
        """
        pass

    def __call__(self) -> None:
        """Sugar for multithreading/multiprocessing.

        Calling any instance of Client will just start `run`.
        """
        return self.run()


class CanbusNet(Client):

    def __init__(self, core_frontend_address: str):
        """Client endpoint for Can Bus communication.

        Args:
            core_frontend_address (str)
        """
        context = zmq.Context.instance()

        self.core_frontend_address = core_frontend_address
        self.identity = u'canbus'

        self.socket = context.socket(zmq.DEALER)
        self.socket.identity = self.identity.encode('ascii')

        self.is_connected = False

    def run(self):
        if not self.connect_to_server():
            print(f"{self.identity} quitting")
            return

        # kept this part alone for simplicity when we setup py can
        try:
            while self.is_connected:
                self.socket.send_json(
                    {"motor": {
                        "temperature": randint(15, 30)
                    }})
                message = self.socket.recv_json()
                print(f"Can Bus received: {message}")
                sleep(1)
        except KeyboardInterrupt:
            self.socket.close()

    def connect_to_server(self) -> bool:
        self.socket.connect(self.core_frontend_address)
        print(f"{self.identity} started, "
              f"connecting to {self.core_frontend_address}")

        if self.register_to_server():
            print(f"{self.identity}: Connection established")
            self.is_connected = True
        else:
            print("CanbusNet: Connection failure")

        return self.is_connected


class PiNet(Client):
    """DEPRECATED: deprecated for a proxy between interface and server.

    We can probably use this as a reference for a testing class.
    """

    def __init__(self, core_frontend_address: str):
        """Client endpoint for user interface communication.

        # TODO: set up websockets, can be done in ZMQ

        Args:
            core_frontend_address (str)
        """
        context = zmq.Context.instance()

        self.core_frontend_address = core_frontend_address
        self.identity = u'ui'

        self.socket = context.socket(zmq.DEALER)
        self.socket.identity = self.identity.encode('ascii')

        self.is_connected = False

    def run(self):
        """Loop for user interface to server connection, primarily through __call__."""
        if not self.connect_to_server():
            print(f"{self.identity} quitting")
            return

        try:
            while True:
                self.socket.send_json(
                    {"climate": {
                        "weathertemperature": randint(15, 30)
                    }})
                message = self.socket.recv_json()
                print(f"UI received: {message}")
                sleep(2)
        except KeyboardInterrupt:
            self.socket.close()

    def connect_to_server(self) -> bool:
        self.socket.connect(self.core_frontend_address)
        print(f"{self.identity} started, "
              f"connecting to {self.core_frontend_address}")

        if self.register_to_server():
            print(f"{self.identity}: Connection established")
            self.is_connected = True
        else:
            print("Pinet: Connection failure")

        return self.is_connected
