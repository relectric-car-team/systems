import zmq

# demo import
from random import randint
from time import sleep

class UserInterfaceTask:
    def __init__(self, core_frontend_address: str):
        """ZMQ Dealer endpoint responsible for UI communication. 

        Args:
            core_frontend_address (str): Address of core's frontend address to connect to.
        """
        self.core_frontend_address = core_frontend_address
        self.identity = u'task-ui0'
    
    def run(self):
        """Start ZMQ Dealer endpoint.
        TODO: Setup websocket communication (can be done through ZMQ). 
        """
        context = zmq.Context.instance()
        socket = context.socket(zmq.DEALER)
        socket.identity = self.identity.encode('ascii')
        socket.connect(self.core_frontend_address)
        print(f"{self.identity} started, connected to {self.core_frontend_address}")

        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        
        while True:
            sleep(2)
            socket.send_json({"temperature": randint(15, 25)})
            incoming_messages = dict(poll.poll())
            if socket in incoming_messages:
                message = socket.recv_json()
                print(f"UI received: {message}")

if __name__ == "__main__":
    user_interface_task = UserInterfaceTask("tcp://127.0.0.1:5001")
    user_interface_task.run()