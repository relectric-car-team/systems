from json.decoder import JSONDecodeError
import zmq
from zmq.decorators import socket
from zmq import Socket
from zmq.utils import jsonapi

from itertools import count



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
    
    @socket(zmq.DEALER)
    def run(self, socket: Socket):
        """Start worker for controller classes. 

        Args:
            socket (Socket): @decorator Dealer socket
        """
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_backend_address)
        print(f"{self.identity} started, connecting to {self.core_backend_address}")

        socket.send(bytes(self.identity, 'utf-8'))
        ready_ping = socket.recv()
        if b'' in ready_ping:
            print(f"{self.identity}: Connection established")

        while True:
            try:
                identity, message = socket.recv_multipart()
            except KeyboardInterrupt:
                return
            
            try:
                message: dict = jsonapi.loads(message)
            except JSONDecodeError:
                continue
            print(f"Worker recieved {message} from {identity}")
            message.update({"processed": True})
            outgoing = jsonapi.dumps(message)
            socket.send_multipart([identity, outgoing])
    

if __name__ == "__main__":
    controller_worker = ControllerWorker("tcp://127.0.0.1:5000")
    controller_worker.run()