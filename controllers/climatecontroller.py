from testdata import*
from canBus import*
from controller import*
class ClimateController(Controller):
    def __init__(self, networkManager):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = canBus()

        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)

    def shutdown(self):   #shutdowns the climatecontroller
        sys.exit()
    def Idle(self):       #updates the controller when the car is in idle
        pass
    def run(self):
        time.sleep(1)
