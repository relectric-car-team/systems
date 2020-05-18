from test import *
from net import *
from controller import *

""" The ClimateController class interfaces with cabin heating and cooling
	systems, performing the necessary consideration to attain the climate settings
	desired by the occupants of the vehicle.
"""
class ClimateController(Controller):
	""" Initializes the ClimateController class by registering actions and
		variables.
	"""
	def __init__(self, networkManager):
		super().__init__(networkManager)
		self.testData = TestData()
		self.testData.loadData()
		self.CANBusController = CANBusNet() # TODO Complete initialization ASAP
		#should the ClimateController have a temperature variable?
		
	""" Safely terminates the ClimateController instance.
	"""
	def shutdown(self):
		sys.exit()

	""" Updates the ClimateController to the current data.
	"""
	def update(self):
		pass

	""" Updates the controller when the car is in idle.
	"""
	def idle(self):
		pass
