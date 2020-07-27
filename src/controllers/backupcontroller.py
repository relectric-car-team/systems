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
        self.testData.update()
        self._register_variable("speed", 0, VariableAccess.READWRITE)
        self._register_variable("distance", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the BackupController instance. """
        super().shutdown()

        self.set_variable("speed", 0)
        self.set_variable("distance", 0)

    def update(self):
        """ Updates the controller to the current data.	"""
        self.set_variable("speed", self.testData.get("speed"))
        self.set_variable("distance", self.testData.get("distance"))
    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01667)
