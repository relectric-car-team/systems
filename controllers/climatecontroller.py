from TestData import*
from canBus import*
from Controller import*
class ClimateController(Controller):
  def __init__(self):
      self.testData = TestData()
      self.testData.loadData()
      self.CANBusController = canBus()

      registerAction("update", update)
      registerAction("shutdown", shutdown)
      #should the climatecontroller have a temperature variable?
  def shutdown(self):

  def update(self):
