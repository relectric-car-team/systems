from threading import Thread

from systems.core import CanbusNet, ControllerWorker, CoreServer, PiNet

# In-proc transports for multi-threaded application, use ipc for multi-processed.
# NOTE: in `inproc` transport, ensure server is started before anything

_frontend_address = "inproc://frontend"
_backend_address = "inproc://backend"


def start_systems():
    """Set up all threads with respective tasks."""
    core_server = CoreServer(_backend_address, _frontend_address)
    controller_worker = ControllerWorker(_backend_address)
    pi_net = PiNet(_frontend_address)
    canbus_net = CanbusNet(_frontend_address)

    server = Thread(target=core_server)
    controllers = Thread(target=controller_worker)
    ui = Thread(target=pi_net)
    canbus = Thread(target=canbus_net)

    tasks = (server, controllers, canbus, ui)
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    start_systems()
