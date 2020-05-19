from test import *
from net import *
from controller import *

""" The BatteryController class interfaces with the batery control module to
    manage charge and discharge activities, as well as providing the driver with
    related feedback on the charge level and expcected range.
"""
class BatteryController(Controller):
    """ Initializes the BatteryController class by registering actions and
        variables.
    """
    def __init__(self, networkManager):
        super().__init__(networkManager)
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = CANBusNet() # TODO Complete initialization ASAP
        # Should the batterycontroller have a voltage variable?
    
    """ Safely terminates the BatteryConrtoller instance.
    """
    def shutdown(self):
        sys.exit()

    """ Updates the batterycontroller to the current data.
    """
    def update(self):
        pass

    """ Updates the controller when the car is in idle.
    """
    def idle(self):
        pass
