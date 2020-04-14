# Standard Imports
import threading
import logging as log
from typing import Union

from arduinoneterror import ArduinoNetError

# Additional Imports
import serial # pip install pyserial


""" ArduinoNet is an asynchronous serial connection wrapper intended for
	communication with Arduino micro controllers over USB. It is important to note
	that due to the nature of Arduino processors, they are unable to communicate
	with external devices over USB without blocking program execution. For this
	reason, it is strongly recommended that any program making use of this class
	operates at the mercy of the Arduino, rather than the letting the Arduino lock
	up pending a transmission.
"""
class ArduinoNet():
	""" Initializes an ArduinoNet object, given the serial device the connection
		is to be made with. The returned object will already be connected and ready
		to send or receive data, provided there were no problems establishing the
		link.

		port - The text identifier of the serial device to be used for the
			connection. Note this port cannot be changed.
	"""
	def __init__(self, port: str) -> None:
		self.__port = port
		self.connect(port)

	""" Establishes the connection with the specified port. Called on 
		initialization by the constructor or after a connection has failed.

	Uncaught - ArduinoNetError 'Unable to establish serial contact.' on
		__establishContact() call.
	"""
	def connect(self) -> None:
		self.__conn = serial.Serial(self.__port, USB_BAUD)
		self.__establishContact()
		self.__conn.timeout = USB_TIMEOUT
		log.info("Serial connection established on port {0}.".format(self.__port))
		self.__running = True

	""" Called to verify a new connection was successful and inform the Arduino
		that a connection has been established correctly.

	Raises ArduinoNetError 'Unable to establish serial contact.' if no response is
		received in the timeout duration.
	"""
	def __establishContact(self) -> None:
		if self.__conn.read() == b'$':
			self.__conn.write(b'$')
		else:
			log.error("Unable to establish serial contact on port {0}.".format(self.__port))
			raise ArduinoNetError("Unable to establish serial contact.")

	""" Sends a value to the Arduino. The value's meaning can be specified by key,
		and integer that is associated with a particular purpose, as determined by
		the implementation using the class. Note that even numbered keys indicate
		data of type int and odd numbers are data of type float.

	data - The value to be sent to the Arduino, either an int or float.
	key - The data descriptor value, an even integer for integers and and odd
		integer for floats. Note that the key must be greater than 0 and less than
		or equal to 65536.

	Raises ArduinoNetError 'Data key out of range.' when the provided key is not
		1 <= k <= 65536.
	Raises ArduinoNetError 'Integer data keys must be even.' if the provided key
		is odd and type(data) == int.
	Raises ArduinoNetError 'Float data keys must be odd.' if the provided key
		is even and type(float) == int.
	"""
	def sendData(self, data: Union[int, float], key: int) -> None:
		if 1 <= key <= 65536:
			payload = key.to_bytes(2, "big")
			if type(data) == int:
				if key % 2 == 0: # Int
					payload = payload + data.to_bytes(2, "big")
				else:
					log.error("Integer data keys must be even.")
					raise ArduinoNetError("Integer data keys must be even.")
			elif type(data) == float:
				if key % 2 == 1: # Float
					payload = payload + data.to_bytes(4, "big")
				else:
					log.error("Float data keys must be odd.")
					raise ArduinoNetError("Float data keys must be odd.")
			st = threading.thread(target=self.__send(), args=(payload))
			st.start()
		else:
			log.error("Data key {0} out of range.".format(key))
			raise ArduinoNetError("Data key out of range.")

	""" Sends a byte payload to the connected Arduino.

	payload - a byte object to be sent to the Arduino.

	Raises ArduinoNetError 'Serial connection failure.' if the connection has been
		lost and the transmission failed.
	"""
	def __send(self, payload: bytes) -> None:
		try:
			self.__conn.write(payload)
		except:
			self.__running = False
			log.error("Serial connection failure on port {0}.".format(self.__port))
			raise ArduinoNetError("Serial connection failure.")

	""" Returns a tuple of the form (value, key) and types ([float|int], int)
		containing the most recent message stored in the serial receive buffer.
	"""
	def getData(self) -> (Union[int, float], int):
		data = None
		try:
			key = self.__conn.read(2)
		except:
			return # TODO
		key = int.from_bytes(key, "big")
		if key % 2 == 0:
			try:
				data = self.__conn.read(2)
			except:
				pass # TODO
		else:
			try:
				data = self.__conn.read(4)
			except:
				pass # TODO
		return data

	""" Informs the Arduino and safely closes the serial connection.
	"""
	def stop(self) -> None:
		try:
			self.__conn.write(bytes(1))
		except:
			pass
		self.__conn.close()
