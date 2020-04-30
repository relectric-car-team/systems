from testdata import*
from canBus import*
from controller import*
import sys
class MotorController(Controller):
    def __init__(self):
        self.testData = TestData()
        self.CANBusController = canBus()
        self.testData.loadData()
        #self.testData.update()
        registerVariable("speed", 0, VariableAccess.READWRITE)
        registerVariable("voltage", 0, VariableAccess.READWRITE)
        registerVariable("temperature", 0, VariableAccess.READWRITE)
        registerVariable("RPM", 0, VariableAccess.READWRITE)

        registerAction("idle", idle)
        registerAction("shutdown", shutdown)
        registerAction("update", update)

    def idle(self):
        setVariable("speed", 0)
        setVariable("RPM", 0)
        #not too sure on what values the voltage and temperature get

    def shutdown(self):
        setVariable("speed", 0)
        setVariable("RPM", 0)
        setVariable("temperature", 0)
        setVariable("voltage", 0)
        sys.exit()

    def update(self):
        setVariable("speed", testData.get(speed))
        setVariable("voltage", testData.get(voltage))
        setVariable("temperature", testData.get(temperature))
        setVariable("RPM", testData.get(RPM))
