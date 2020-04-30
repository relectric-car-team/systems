from testdata import*
from canBus import*
from controller import*
class ClimateController(Controller):
    def __init__(self):
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = canBus()

        registerAction("update", update)
        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)
      #should the climatecontroller have a temperature variable?
    def shutdown(self):   #shutdowns the climatecontroller
        sys.exit()
    def update(self):     #updates the climatecontroller to the current data
        pass
    def Idle(self):       #updates the controller when the car is in idle
      pass
        pass
