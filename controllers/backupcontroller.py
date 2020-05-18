from test import *
from controller import *

""" The BackupController class interfaces with the rear sensor hardware
	controllers to alert the driver if the vehicle is at rick of backing into an
	obstacle.
"""
class BackupController(Controller):
	""" Initializes the BackupController class by registering actions and
		variables.
	"""
	def __init__(self, networkManager):	
		super().__init__(networkManager)
		self.testData = TestData()
		self.testData.loadData()

	""" Safely terminates the BackupController instance.
	"""
	def shutdown(self):
		sys.exit()

	""" Updates the controller to the current data.
	"""
	def update(self):
		pass

	""" Updates the controller when the car is in idle.
	"""
	def idle(self):
		pass
