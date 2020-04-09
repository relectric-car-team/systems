class ClimateController():
  TestData testData
  canBus CANBusController
  def __init__(self):
      testData.loadData()
      CANBusController = new canBus()
