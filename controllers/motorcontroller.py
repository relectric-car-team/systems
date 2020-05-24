from test import *
from net import *
from controller import *


class MotorController(Controller):
    """ The MotorController class interfaces with the motor drive to obtain
    telemetry.
    """

    def __init__(self, network_manager):
        """ Initializes the MotorController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.testData = TestData()
        self.CANBusController = CANBusNet()  # TODO Complete initialization ASAP
        # self.testData.update()
        self.__register_variable("speed", 0, VariableAccess.READWRITE)
        self.__register_variable("voltage", 0, VariableAccess.READWRITE)
        self.__register_variable("temperature", 0, VariableAccess.READWRITE)
        self.__register_variable("RPM", 0, VariableAccess.READWRITE)

    def idle(self):
        """ Updates the controller when the car is in idle.	"""
        self.set_variable("speed", 0)
        self.set_variable("RPM", 0)
        # Not too sure on what values the voltage and temperature get

    def shutdown(self):
        """ Safely terminates the MotorController instance. """
        self.set_variable("speed", 0)
        self.set_variable("RPM", 0)
        self.set_variable("temperature", 0)
        self.set_variable("voltage", 0)

    def update(self):
        """ Updates the controller to the current data.	"""
        self.set_variable("speed", self.testData.get("speed"))
        self.set_variable("voltage", self.testData.get("voltage"))
        self.set_variable("temperature", self.testData.get("temperature"))
        self.set_variable("RPM", self.testData.get("RPM"))
