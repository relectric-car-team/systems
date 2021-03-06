import zmq
from zmq import Socket
from zmq.decorators import socket
from core.abstract import Client

# demo import
from random import randint
from time import sleep


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
        print(f"{self.identity} started, connecting to {self.core_frontend_address}")

        if self.ping_server(socket):
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

        
if __name__ == "__main__":
    canbus_net = CanbusNet("tcp://127.0.0.1:5001")
    canbus_net.run()