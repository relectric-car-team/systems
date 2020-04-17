# Imports
from net import PiNet, ArduinoNet

""" NetworkManager takes ownsership of all networking library objects so that
	instances of controller classes may use them. Passing this class down to the
	controller classes ensures they do not use duplicates of these networking
	interfaces.
"""
class NetworkManager():
	""" Initializes NetworkManager and creates and starts all of the network
		interfaces.
	"""
	def __init__(self):
		self.__pinet = PiNet(True, ("localhost", 4000))

	""" Returns the active PiNet instance.
	"""
	def getPiNet(self) -> PiNet:
		pass

	""" Returns the active ArduinoNet instance.
	"""
	def getArduinoNet(self, port: int) -> ArduinoNet:
		pass

	""" Safely closes all network interfaces.
	"""
	def stop(self) -> None:
		pass
