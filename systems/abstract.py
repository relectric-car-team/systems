from abc import ABC, abstractmethod

from zmq import Socket


class Client(ABC):
    core_frontend_address: str
    identity: str
    socket: Socket
    is_connected = False

    def register_to_server(self,
                           socket: Socket,
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
    def run(self, socket: Socket) -> None:
        """Start main routine for ZMQ client endpoint.

        Mainly done through __call__().
        """
        pass    # TODO: set up retry system

    def __call__(self) -> None:
        """Sugar for multithreading/multiprocessing.

        Calling any instance of Client will just start `run`.
        """
        return self.run()
