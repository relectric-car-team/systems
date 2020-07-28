import time
from test import TestData
from controller import Controller


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
        self.test_data = TestData()

    def shutdown(self):
        """ Safely terminates the BackupController instance. """
        super().shutdown()

    def update(self):
        """ Updates the controller to the current data.	"""
        pass

    def _run(self):
        """ Run loop for the controller """
        time.sleep(1)
