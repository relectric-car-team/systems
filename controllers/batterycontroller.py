class BatteryController():
  TestData testData
  canBus CANBusController
  def __init__(self):
      testData.loadData()
      CANBusController = new canBus() #uhm not sure what or how to initialize this
