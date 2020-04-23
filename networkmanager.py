# Imports
from typing import List

from net import PiNet, ArduinoNet

""" NetworkManager takes ownership of all networking library objects so that
	instances of controller classes may use them. Passing this class down to the
	controller classes ensures they do not use duplicates of these networking
	interfaces.
"""
class NetworkManager():
	""" Initializes NetworkManager and creates and starts all of the network
		interfaces.

		serial_ports - A list containing the platform identifiers (strings) for the
			serial ports to be bound. The index of the identifier is the same as the
			integer used to retrieve a the respective ArduinoNet instance with
			getArduinoNet(). Example identifiers include 'COM3' for Windows and
			'/dev/ttyUSB0' for GNU/Linux.
	"""
	def __init__(self, serial_ports: List[str]) -> None:
		self.__pinet = PiNet(True, ("localhost", 4000)) # Assuming we use this port
		self.__arduinonets = []
		for i in serial_ports:
			self.__arduinonets.append(ArduinoNet(i))

	""" Returns the active PiNet instance.
	"""
	def getPiNet(self) -> PiNet:
		return self.__pinet

	""" Returns the active ArduinoNet instance.
	port - An integer specifying the serial port tied to the ArduinoNet instance
		being requested. See __init__().
	"""
	def getArduinoNet(self, port: int) -> ArduinoNet:
		return self.__arduinonet

	""" Returns the active CANBusNet instance.
	"""
	# ==== The following is commented until a template of CANBusNet can be made.
	#def getCANBusNet(self) -> CANBusNet:
	#	pass

	""" Safely closes all network interfaces.
	"""
	def stop(self) -> None:
		self.__pinet.stop()
		for port in self.__arduinonets:
			port.stop()
