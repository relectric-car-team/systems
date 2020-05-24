from test import *
from controller import *


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

    def shutdown(self):
        """ Safely terminates the BackupController instance. """
        pass

    def update(self):
        """ Updates the controller to the current data.	"""
        pass

    def idle(self):
        """ Updates the controller when the car is in idle. """
        pass
