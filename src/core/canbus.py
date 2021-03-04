import zmq
from itertools import count

# demo import
from random import randint
from time import sleep


class CanbusTask:
    _count = count(0)
    def __init__(self, core_backend_address: str):
        """ZQM Dealer responsible for Can Bus communication. 
        Currently non-functional. 

        Args:
            core_backend_address (str): Address of core's backend address to connect to. 
        """
        self.core_backend_address = core_backend_address
        self.identity = u'task-canbus{}'.format(self._count)
        self._count = next(self._count)
    
    def run(self):
        """Start ZMQ Dealer endpoint.
        """
        context = zmq.Context.instance()
        socket = context.socket(zmq.DEALER)
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_backend_address)
        print(f"{self.identity} started, connected to {self.core_backend_address}")
        
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)

        while True:
            sleep(2)
            socket.send_json({"speed": randint(10, 100)})
            incoming_messages = dict(poll.poll()) # NOTE: we can set timeout here if needed
            if socket in incoming_messages:
                message = socket.recv_json()
                print(f"Canbus received: {message}")


        
if __name__ == "__main__":
    canbus_task = CanbusTask("tcp://127.0.0.1:5000")
    canbus_task.run()