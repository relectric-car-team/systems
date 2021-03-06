import zmq
from zmq.decorators import socket
from zmq import Socket

from core.abstract import Client

# demo import
from random import randint
from time import sleep


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
        print(f"{self.identity} started, connecting to {self.core_frontend_address}")

        if self.ping_server(socket):
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
        
        

if __name__ == "__main__":
    pi_net = PiNet("tcp://127.0.0.1:5001")
    pi_net.run()