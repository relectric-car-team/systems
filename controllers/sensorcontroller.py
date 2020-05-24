from test import *
from controller import *


class SensorController(Controller):
    """ The SensorController class communicates with sensors throughout the
    vehicle to inform the operation of its systems and keep the driver updated
    on the car's condition.
    """

    def __init__(self, network_manager):
        """ Initializes the SensorController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.testData = TestData()

    def shutdown(self):
        """ Safely terminates the SensorController instance. """
        pass

    def update(self):
        """ Updates the SensorController to the current data. """
        pass

    def idle(self):
        """ Updates the controller when the car is in idle.	"""
        pass
