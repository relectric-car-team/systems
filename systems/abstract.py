from abc import ABC, abstractmethod

from zmq import Socket
from zmq.decorators import socket


class Client(ABC):
    core_frontend_address: str
    identity: str
    is_vibe_checked: bool = False

    def vibe_check_server(self, socket: Socket) -> bool:
        """Vibe check server for synchronized start.

        Args:
            socket (Socket)

        Returns:
            bool: True if connection granted
        """
        socket.send(b'')
        ready_ping = socket.recv_multipart()
        self.is_vibe_checked = b'' in ready_ping
        return self.is_vibe_checked

    @socket()
    @abstractmethod
    def run(self, socket: Socket) -> None:
        """Start main routine for ZMQ client endpoint.

        Mainly done through __call__().

        Args:
            socket (Socket): @decorator ZMQ Socket
        """
        pass    # TODO: set up retry system

    def __call__(self) -> None:
        """Sugar for multithreading/multiprocessing.

        Calling any instance of Client will just start `run`.
        """
        return self.run()
