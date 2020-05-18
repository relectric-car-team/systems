from testdata import*
from controller import*
class SensorController(Controller):
    def __init__(self, networkManager):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()

        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)

    def shutdown(self):   #shutdowns the SensorController
        sys.exit()
    def Idle(self):       #updates the controller when the car is in idle
        pass
    def run(self):
        pass
