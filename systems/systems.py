from core import CoreServer, CanbusNet, PiNet, ControllerWorker
from threading import Thread

# In-proc transports for multi-threaded application, use ipc for multi-processed.
# NOTE: in `inproc` transport, ensure server is started before anything

_frontend_address = "inproc://frontend"
_backend_address = "inproc://backend"

def init_tasks():
    """Set up all threads with respective tasks.
    """
    core_server = CoreServer(_backend_address, _frontend_address)
    controller_worker = ControllerWorker(_backend_address)
    pi_net = PiNet(_frontend_address)
    canbus_net = CanbusNet(_frontend_address)

    server = Thread(target=core_server.run)
    controllers = Thread(target=controller_worker.run)
    ui = Thread(target=pi_net)
    canbus = Thread(target=canbus_net)

    tasks = (server, controllers, canbus, ui)
    for task in tasks:
        task.start()
    
    for task in tasks:
        task.join()

if __name__ == "__main__":
    init_tasks()