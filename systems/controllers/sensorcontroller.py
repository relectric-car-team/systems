import time
from test import TestData
from controller import Controller
from controllerdata import VariableAccess


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
        self.test_data = TestData("test/data/sensorData.csv")
        self._register_variable("distanceFront", 0, VariableAccess.READWRITE)
        self._register_variable("distanceBack", 0, VariableAccess.READWRITE)

    def shutdown(self):
        """ Safely terminates the SensorController instance. """
        super().shutdown()
        self.set_variable("distanceFront", 0)
        self.set_variable("distanceBack", 0)

    def update(self):
        """ Updates the SensorController to the current data. """
        self.set_variable("distanceFront", self.test_data.get("distanceFront"))
        self.set_variable("distanceBack", self.test_data.get("distanceBack"))
        self.test_data.update()

    def _run(self):
        """ Run loop for the controller """
        time.sleep(0.01666667)
        self.update()
