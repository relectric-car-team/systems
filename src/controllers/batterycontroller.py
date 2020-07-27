import time
from test import TestData
from net import CANBusNet
from controller import Controller


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
        self.test_data = TestData()
        self.can_bus_controller = CANBusNet()  # TODO Complete initialization ASAP
        # Should the BatteryController have a voltage variable?

    def shutdown(self):
        """ Safely terminates the BatteryController instance. """
        super().shutdown()

    def update(self):
        """ Updates the BatteryController to the current data. """
        pass

    def _run(self):
        """ Run loop for the controller """
        time.sleep(1)
