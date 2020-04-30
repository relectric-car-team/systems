from testdata import*
from controller import*
class SensorController(Controller, networkManager):
    def __init__(self):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()

        registerAction("update", update)
        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)

    def shutdown(self):   #shutdowns the SensorController
        sys.exit()
    def update(self):     #updates the SensorController to the current data
        pass
    def Idle(self):       #updates the controller when the car is in idle
        pass
