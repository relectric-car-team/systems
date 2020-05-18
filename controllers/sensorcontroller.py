from test import *
from controller import *

""" The SensorController class communicates with sensors throughout the vehicle
	to inform the operation of its systems and keep the driver updated on the
	car's condition.
"""
class SensorController(Controller):
	""" Initializes the SensorController class by registering actions and
		variables.
	"""
	def __init__(self, networkManager):
		super().__init__(networkManager)
		self.testData = TestData()
		self.testData.loadData()

	""" Safely terminates the SensorController instance.
	"""
	def shutdown(self):
		sys.exit()

	""" Updates the SensorController to the current data.
	"""
	def update(self):
		pass

	""" Updates the controller when the car is in idle.
	"""
	def idle(self):
		pass
