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
        self.testData.update()
        self._register_variable("voltage", 0, VariableAccess.READWRITE)
        self._register_variable("temperature", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the BatteryController instance. """
        super().shutdown()

        self.set_variable("voltage", 0)
        self.set_variable("temperature", 0)

    def update(self):
        """ Updates the BatteryController to the current data. """
        self.set_variable("voltage", self.testData.get("voltage"))
        self.set_variable("temperature", self.testData.get("temperature"))

    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01667)
