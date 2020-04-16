from TestData import*
from canBus import*
from Controller import*
class BatteryController(Controller):
  def __init__(self):
     self.testData = TestData()
     self.testData.loadData()
     self.CANBusController = canBus() #uhm not sure what or how to initialize this

     registerAction("shutdown", shutdown)
     registerAction("update", update)

     #should the batterycontroller have a voltage variable?
  def shutdown(self):

  def update(self):
