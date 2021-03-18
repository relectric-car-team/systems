from threading import Thread

from systems.clients import CanbusNet, PiNet
from systems.core import BrowserProxy, ControllerWorker, CoreServer

# In-proc transports for multi-threaded application, use ipc for multi-processed.
# NOTE: in `inproc` transport, ensure server is started before anything

_frontend_address = "inproc://frontend"
_backend_address = "inproc://backend"
_browser_address = "ws://127.0.0.1:8001"


def start_systems():
    """Set up all threads with respective tasks."""
    core_server = CoreServer(_backend_address, _frontend_address)
    controller_worker = ControllerWorker(_backend_address)
    browser_proxy = BrowserProxy(_frontend_address, _browser_address)
    pi_net = PiNet(_browser_address)
    canbus_net = CanbusNet(_frontend_address)

    server = Thread(target=core_server)
    controllers = Thread(target=controller_worker)
    browser = Thread(target=browser_proxy)
    ui = Thread(target=pi_net)
    canbus = Thread(target=canbus_net)

    tasks = (
        server,
        controllers,
        browser,
        canbus,
        ui,
    )
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    start_systems()
