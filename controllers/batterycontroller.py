from test import *
from net import *
from controller import *
import time


class BatteryController(Controller):
    """ The BatteryController class interfaces with the battery control
    module to manage charge and discharge activities, as well as providing
    the driver with related feedback on the charge level and expected range.
    """

    def __init__(self, network_manager):
        """ Initializes the BatteryController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.testData = TestData()
        self.CANBusController = CANBusNet()  # TODO Complete initialization ASAP
        # Should the BatteryController have a voltage variable?

    def shutdown(self):
        """ Safely terminates the BatteryController instance. """
        super().shutdown()

    def update(self):
        """ Updates the BatteryController to the current data. """
        pass

    def run(self):
        time.sleep(1)
