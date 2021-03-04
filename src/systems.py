from time import sleep
from core import Proxy, CanbusTask, UserInterfaceTask
from threading import Thread

# In-proc transports for multi-threaded application, use ipc for multi-processed.
# NOTE: if using In-proc, start binded endpoints (proxy) first.
_frontend_address = "inproc://frontend"
_backend_address = "inproc://backend"

def init_tasks():
    """Set up all threads with respective tasks.
    """
    canbus_io = CanbusTask(_backend_address)
    proxy = Proxy(_backend_address, _frontend_address)
    user_interface_io = UserInterfaceTask(_frontend_address)

    proxy_task = Thread(target=proxy.run)
    canbus_task = Thread(target=canbus_io.run)
    user_interface_task = Thread(target=user_interface_io.run)

    tasks = (proxy_task, canbus_task, user_interface_task)
    for task in tasks:
        task.start()
    

    for task in tasks:
        task.join()

if __name__ == "__main__":
    init_tasks()