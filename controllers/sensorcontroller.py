from test import *
from controller import *

""" 
"""
class SensorController(Controller):
	""" 
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
