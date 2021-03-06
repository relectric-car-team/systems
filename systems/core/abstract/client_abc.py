from abc import ABC, abstractmethod

from zmq import Socket
from zmq.decorators import socket

class Client(ABC):
    core_frontend_address: str
    identity: str

    @staticmethod
    def ping_server(socket: Socket) -> bool:
        """Ping server for synchronized start. 

        Args:
            socket (Socket)

        Returns:
            bool: True if connection granted
        """
        socket.send(b'')
        ready_ping = socket.recv_multipart()
        return (b'' in ready_ping)

    @socket()
    @abstractmethod
    def run(self, socket: Socket) -> None:
        """Start main routine for ZMQ client endpoint. 

        Args:
            socket (Socket): @decorator ZMQ Socket
        """
        pass # TODO: set up retry system

    def __call__(self) -> None:
        """Sugar for multithreading/multiprocessing. 
        Calling any instance of Client will just start `run`.
        """
        return self.run()