import time
from test import TestData
from net import CANBusNet
from controller import Controller


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
        self.test_data = TestData("data/climateData.csv")
        self.can_bus_controller = CANBusNet()  # TODO Complete initialization ASAP
        # Should the ClimateController have a temperature variable?
        self._register_variable("weatherTemp", 0, VariableAccess.READWRITE)
        self._register_variable("fanPower", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the ClimateController instance. """
        super().shutdown()
        self.set_variable("weatherTemp", 0)
        self.set_variable("fanPower", 0)

    def update(self):
        """ Updates the ClimateController to the current data. """
        self.set_variable("weatherTemp", self.test_data.get("weatherTemp"))
        self.set_variable("fanPower", self.test_data.get("fanPower"))
        self.test_data.update()

    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01666667)
        self.update()
