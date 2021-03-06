import zmq
from zmq import Socket
from zmq.decorators import socket

class CoreServer:
    def __init__(self, backend_binding: str, frontend_binding: str):
        """Basic ZMQ server for communication between frontend clients and backend workers. 

        Args:
            backend_binding (str): Address of backend binding
            frontend_binding (str): Address of frontend binding
        """
        self.backend_binding = backend_binding
        self.frontend_binding = frontend_binding

    @socket(zmq.ROUTER)
    @socket(zmq.DEALER)
    def run(self, frontend: Socket, backend: Socket):
        """Start core server to facilitate client to worker communications. 

        Args:
            frontend (Socket): @decorator Router socket
            backend (Socket): @decorator Dealer socket
        """
        frontend.bind(self.frontend_binding)
        backend.bind(self.backend_binding)

        poller = zmq.Poller()
        poller.register(backend, zmq.POLLIN)
        poller.register(frontend, zmq.POLLIN)

        print("Server setup finished")

        worker_ids = set()
        client_identities = set()

        while (len(client_identities) < 2) or (len(worker_ids) < 1):
            try:
                pings = dict(poller.poll())
            except KeyboardInterrupt:
                return
            
            if frontend in pings:
                [client_identity, _] = frontend.recv_multipart()
                client_identities.add(client_identity)
                print(f"{client_identity} connected")

            if backend in pings:
                worker_id = backend.recv()
                worker_ids.add(worker_id)
                print(f"Worker @ {worker_id} connected")
            
        backend.send(b'')
        print(f"{len(worker_ids)} worker(s) ready")
        
        for client in client_identities:
            frontend.send_multipart([client, b''])
        print(f"Server initialized, connected to {client_identities}")

        while True:
            try:
                incoming_messages = dict(poller.poll())
            except KeyboardInterrupt:
                return 
            
            if frontend in incoming_messages:
                message = frontend.recv_multipart()
                backend.send_multipart(message, zmq.NOBLOCK)
            
            if backend in incoming_messages:
                message = backend.recv_multipart()
                frontend.send_multipart(message)



if __name__ == "__main__":
    core_server = CoreServer("tcp://127.0.0.1:5000", "tcp://127.0.0.1:5001")
    core_server.run()