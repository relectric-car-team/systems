from test import *
from net import *
from controller import *
import time

class ClimateController(Controller):
    """ The ClimateController class interfaces with cabin heating and cooling
    systems, performing the necessary consideration to attain the climate
    settings desired by the occupants of the vehicle.
    """

    def __init__(self, network_manager):
        """ Initializes the ClimateController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.testData = TestData()
        self.CANBusController = CANBusNet()  # TODO Complete initialization ASAP
        # Should the ClimateController have a temperature variable?

    def shutdown(self):
        """ Safely terminates the ClimateController instance. """
        super().shutdown()

    def update(self):
        """ Updates the ClimateController to the current data. """
        pass

    def run(self):
        time.sleep(1)
