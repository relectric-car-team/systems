import sys object
class MotorController():
    TestData testData
    canBus CANBusController
    double speed
    double voltage
    double temperature
    double RPM

    def __init__(self):
        testData.loadData()
        CANBusController = new canBus()
        speed = testData.get("speed")
        voltage = testData.get("voltage")
        temperature = testData.get("temperature")
        RPM = testData.get("RPM")
        Stop()
        Shutdown()


    def Stop(self):
        exit()
    def Shutdown(self):
        pass
