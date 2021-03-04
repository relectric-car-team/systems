import zmq


class Proxy:
    def __init__(self, backend_binding: str, frontend_binding: str):
        """Basic ZMQ Proxy for full-duplex communication between frontend, backend. 

        Args:
            backend_binding (str): Address of backend binding. 
            frontend_binding (str): Address of frontend binding.
        """
        self.backend_binding = backend_binding
        self.frontend_binding = frontend_binding

    def run(self):
        """Start ZMQ Proxy endpoint.
        """
        context = zmq.Context.instance()

        frontend_socket = context.socket(zmq.DEALER)
        frontend_socket.bind(self.frontend_binding)

        backend_socket = context.socket(zmq.DEALER)
        backend_socket.bind(self.backend_binding)
        
        print("Core initialized, listening")

        zmq.proxy(frontend_socket, backend_socket)



if __name__ == "__main__":
    proxy = Proxy("tcp://127.0.0.1:5000", "tcp://127.0.0.1:5001")
    proxy.run()