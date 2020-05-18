from test import *
from net import *
from controller import *
import sys

""" The MotorController class interfaces with the motor drive to obtain
	telemetry.
"""
class MotorController(Controller):
	""" Initializes the MotorController class by registering actions and
		variables.
	"""
	def __init__(self, networkManager):
		super().__init__(networkManager)
		self.testData = TestData()
		self.CANBusController = CANBusNet() # TODO Complete initialization ASAP
		self.testData.loadData()
		#self.testData.update()
		self.registerVariable("speed", 0, VariableAccess.READWRITE)
		self.registerVariable("voltage", 0, VariableAccess.READWRITE)
		self.registerVariable("temperature", 0, VariableAccess.READWRITE)
		self.registerVariable("RPM", 0, VariableAccess.READWRITE)

	""" Updates the controller when the car is in idle.
	"""
	def idle(self):
		self.setVariable("speed", 0)
		self.setVariable("RPM", 0)
		#not too sure on what values the voltage and temperature get

	""" Safely terminates the MotorController instance.
	"""
	def shutdown(self):
		self.setVariable("speed", 0)
		self.setVariable("RPM", 0)
		self.setVariable("temperature", 0)
		self.setVariable("voltage", 0)
		sys.exit()

	""" Updates the controller to the current data.
	"""
	def update(self):
		self.setVariable("speed", testData.get(speed))
		self.setVariable("voltage", testData.get(voltage))
		self.setVariable("temperature", testData.get(temperature))
		self.setVariable("RPM", testData.get(RPM))
