import time
from test import TestData
from controller import Controller


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
        self.test_data = TestData()

    def shutdown(self):
        """ Safely terminates the SensorController instance. """
        super().shutdown()
        pass

    def update(self):
        """ Updates the SensorController to the current data. """
        pass

    def _run(self):
        """ Run loop for the controller """
        time.sleep(1)
