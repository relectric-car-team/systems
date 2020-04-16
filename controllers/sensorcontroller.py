from TestData import*
from Controller import*
class SensorController(Controller):
  def __init__(self):
      self.testData = TestData()
      self.testData.loadData()

      registerAction("update", update)
      registerAction("shutdown", shutdown)
  def shutdown(self):

  def update(self):
