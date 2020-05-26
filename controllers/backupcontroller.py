from test import *
from controller import *
import time
class BackupController(Controller):
    """ The BackupController class interfaces with the rear sensor hardware
    controllers to alert the driver if the vehicle is at rick of backing into an
    obstacle.
    """

    def __init__(self, network_manager):
        """ Initializes the BackupController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.testData = TestData()

        self._register_action("shutdown", shutdown)
        self._register_action("idle", idle)

    def shutdown(self):
        """ Safely terminates the BackupController instance. """
        super().shutdown()

    def update(self):
        """ Updates the controller to the current data.	"""
        pass

    def run(self):
        """ Run loop for the controller """
        time.sleep(1)
