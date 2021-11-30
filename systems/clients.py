from abc import ABC, abstractmethod
from platform import machine
from random import randint
from time import sleep

import zmq
from loguru import logger

from systems.controllers import Message

if ("armv" in machine()):    # if machine is rpi, import spidev
    import spidev


class Client(ABC):
    core_frontend_address: str
    identity: str
    socket: zmq.Socket

    @abstractmethod
    def run(self) -> None:
        """Start main routine for ZMQ client endpoint.

        Mainly done through __call__().
        """
        pass

    def register_to_server(self, ready_message: bytes = b'ready') -> bool:
        """Vibe check server for synchronized start.

        Args:
            ready_message (bytes, optional): Defaults to b'ready'.

        Returns:
            bool: True if connection granted.
        """
        self.socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = self.socket.recv()
        return ready_message in ready_ping

    @abstractmethod
    def connect_to_server(self) -> bool:
        """Connect and register to server.

        Returns:
            bool: True if connection successful.
        """
        pass

    def __call__(self) -> None:
        """Handles graceful exiting and sugar for Thread() syntax.

        Calling any instance of Client will just start `run`.
        """
        try:
            self.run()
        except KeyboardInterrupt:
            self.socket.close()


class CanbusNet(Client):

    def __init__(self, core_frontend_address: str):
        """Client endpoint for Can Bus communication.

        Args:
            core_frontend_address (str).
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

        while True:
            if ("armv" in machine()):    # checks if python is running in a rpi
                speed = self.get_spi("s")
                if (speed == -1):
                    speed = randint(50, 100)
                voltage = self.get_spi("v")
                if (voltage == -1):
                    voltage = randint(50, 100)
            else:
                speed = randint(50, 100)
                voltage = randint(50, 100)
            message = Message(controller="MotorController",
                              data={
                                  "speed": speed,
                                  "voltage": voltage
                              },
                              destinations=[['browser', 'ui'], ['canbus']])
            self.socket.send_json(message)
            incoming_message: Message = self.socket.recv_json()
            logger.debug(f"Can Bus received: {incoming_message}")
            sleep(1)

    def get_spi(self, mode) -> int:
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 1000000
        recieved_byte = spi.xfer2([ord('s')])
        sleep(0.5)
        if ((recieved_byte[0] == 0) or (recieved_byte[0] == 255)):
            spi.close()
            return -1
        spi.close()
        return recieved_byte[0]

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
            dummy_message = Message(controller="BatteryController",
                                    data={"percentage": randint(40, 50)},
                                    destinations=[['canbus']])
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

    def register_to_server(self, ready_message: bytes = b'ready') -> bool:
        self.socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = self.socket.recv()
        return ready_message in ready_ping
