from testdata import*
from canBus import*
from controller import*
class BatteryController(Controller):
    def __init__(self, networkManager):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = canBus() #uhm not sure what or how to initialize this

        registerAction("shutdown", shutdown)
        registerAction("update", update)
        registerAction("Idle", Idle)

     #should the batterycontroller have a voltage variable?
     def shutdown(self):   #shutdowns the batterycontroller
        sys.exit()
     def update(self):     #updates the batterycontroller to the current data
        pass
     def Idle(self):       #updates the controller when the car is in idle
        pass
