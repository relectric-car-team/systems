from testdata import*
from canBus import*
from controller import*
class BatteryController(Controller):
    def __init__(self, networkManager):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = canBus()

        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)


     def shutdown(self):   #shutdowns the batterycontroller
        sys.exit()

     def Idle(self):       #updates the controller when the car is in idle
        pass

    def run(self):
        pass
