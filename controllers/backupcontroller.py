from TestData import*
from Controller import*
class BackupController(Controller):
  def __init__(self):
      self.testData = TestData()
      self.testData.loadData()

      registerAction("shutdown", shutdown)
      registerAction("update", update)


  def shutdown(self):

  def update(self):
