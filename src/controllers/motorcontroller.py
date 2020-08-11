import time
from test import TestData
from net import CANBusNet
from controller import Controller, VariableAccess


class MotorController(Controller):
    """ The MotorController class interfaces with the motor drive to obtain
    telemetry.
    """

    def __init__(self, network_manager):
        """ Initializes the MotorController class by registering actions and
        variables.
        """
        super().__init__(network_manager)
        self.test_data = TestData("data/MotorControllerTestData.csv")
        self.can_bus_controller = CANBusNet()  # TODO Complete initialization ASAP
        self.testData.update()
        self._register_variable("speed", 0, VariableAccess.READWRITE)
        self._register_variable("voltage", 0, VariableAccess.READWRITE)
        self._register_variable("temperature", 0, VariableAccess.READWRITE)
        self._register_variable("RPM", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the MotorController instance. """
        super().shutdown()

        self.set_variable("speed", 0)
        self.set_variable("RPM", 0)
        self.set_variable("temperature", 0)
        self.set_variable("voltage", 0)

    def update(self):
        """ Updates the controller to the current data.	"""
        self.set_variable("speed", self.test_data.get("speed"))
        self.set_variable("voltage", self.test_data.get("voltage"))
        self.set_variable("temperature", self.test_data.get("temperature"))
        self.set_variable("RPM", self.test_data.get("RPM"))

    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01667)
