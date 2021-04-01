from abc import ABC, abstractmethod
from random import randint
from time import sleep

import zmq
from loguru import logger

from .controllers import Message


class Client(ABC):
    core_frontend_address: str
    identity: str
    socket: zmq.Socket

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
        """Handles graceful exiting and sugar for Thread() syntax.

        Calling any instance of Client will just start `run`.
        """
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        self.socket.close()


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

    def run(self):
        if not self.connect_to_server():
            logger.info(f"{self.identity} quitting")
            return

        # kept this part alone for simplicity when we setup py can
        while True:
            dummy_message = Message(controller="MotorController",
                                    data={
                                        "speed": randint(50, 100),
                                        "voltage": randint(20, 40),
                                        "temperature": randint(50, 100)
                                    })
            self.socket.send_json(dummy_message)
            incoming_message: Message = self.socket.recv_json()
            logger.debug(f"Can Bus received: {incoming_message}")
            sleep(1)

    def connect_to_server(self) -> bool:
        self.socket.connect(self.core_frontend_address)
        logger.info(f"{self.identity} started, "
                    f"connecting to {self.core_frontend_address}")

        if self.register_to_server():
            logger.success(f"{self.identity}: Connection established")
            return True
        else:
            logger.error("CanbusNet: Connection failure")
            return False


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

    def run(self):
        """Loop for user interface to server connection, primarily through __call__."""
        if not self.connect_to_server():
            logger.info(f"{self.identity} quitting")
            return

        while True:
            dummy_message = [
                Message(controller="BatteryController",
                        data={"percentage": randint(40, 50)}),
                Message(controller="ClimateController",
                        data={
                            "fanPower": randint(0, 4),
                            "temperatureSetting": randint(50, 100)
                        })
            ]
            self.socket.send_json(dummy_message)
            incoming_message: Message = self.socket.recv_json()
            logger.debug(f"UI received: {incoming_message}")
            sleep(2)

    def connect_to_server(self) -> bool:
        self.socket.connect(self.core_frontend_address)
        logger.info(f"{self.identity} started, "
                    f"connecting to {self.core_frontend_address}")

        if self.register_to_server():
            logger.success(f"{self.identity}: Connection established")
            return True
        else:
            logger.error("Pinet: Connection failure")
            return False
