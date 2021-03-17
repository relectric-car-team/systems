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

    def register_to_server(self,
                           socket: zmq.Socket,
                           ready_message: str = b'') -> bool:
        """Vibe check server for synchronized start.

        Args:
            socket (Socket)
            ready_message (str, optional): Defaults to b''.

        Returns:
            bool: True if connection granted
        """
        socket.send(b'')
        ready_ping = socket.recv_multipart()
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

        if self.register_to_server(self.socket):
            print(f"{self.identity}: Connection established")
            self.is_connected = True
        else:
            print("Connection failure")

        return self.is_connected


class PiNet(Client):

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

        if self.register_to_server(self.socket):
            print(f"{self.identity}: Connection established")
            self.is_connected = True
        else:
            print("Connection failure")

        return self.is_connected
