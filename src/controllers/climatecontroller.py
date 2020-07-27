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
        self._register_variable("weatherTemp", 0, VariableAccess.READWRITE)
        self._register_variable("fanPower", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the ClimateController instance. """
        super().shutdown()
        self.set_variable("weatherTemp", 0)
        self.set_variable("fanPower", 0)
        
    def update(self):
        """ Updates the ClimateController to the current data. """
        self.set_variable("weatherTemp", self.testData.get("temperature"))
        self.set_variable("fanPower", self.testData.get("fanPower"))

    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01666667)
