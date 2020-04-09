# Standard Imports
import socket
import threading
import json
import random
import time
import logging as log
from typing import Union, List, Dict

# Additional Imports
import serial # pip install pyserial

# Constants
NETWORK_TIMEOUT = 0.1
USB_BAUD = 19200 # 2.4kb/s
USB_TIMEOUT = NETWORK_TIMEOUT


""" The standard exception type to be thrown by instances of PiNet at runtime.
"""
class PiNetError(Exception):
	pass


""" The standard exception type to be thrown by instances of ArduinoNet at runtime.
"""
class ArduinoNetError(Exception):
	pass


""" Encapsulates data to facilitate ownership by local software and usage for
	data requests by peers in the PiNet and ArduinoNet classes.

As Python python does not have C/C++ style pointers, it is necessary to pass
	variables by reference in order for the caller of this module to maintain
	ownership of them. The NetData class is to be instantiated by the caller and
	provided to instances of PiNet or ArduinoNet with the RegisterNetDataObj()
	methods.
"""
class NetData:
	""" Constructs and instance of the NetData class.

	name - A string representing the data housed by the object. Peers will
		refer to specific variables by this name.
	value - The object to be held by this instance. value should only be a basic
		data type available in Python.
	"""
	def __init__(self, name: str, value: any) -> None:
		self.name = name
		self.value = value


""" PiNet is an asynchronous socket wrapper to facilitate communications between
	different Raspberry Pi computers (and indeed other computers). The class is
	intended to facilitate easy communication over LAN using JSON encoding.
	Furthermore, all networking operations are designed to run in separate threads
	to that of the dispatching main program, preventing lockups and allowing time
	critical execution to continue unaffected.
"""
class PiNet:
	""" Constructs a new instance of PiNet.

	isServer - A boolean value indicating if the new PiNet object is to be a
		server (True) or a client (False).
	address - The network address to bind the connection to.
	port - The network port the PiNet will create connections with. Must be
		between 0 and 65535 inclusive.

	Raises PiNetError "Invalid port." when the provided port is not within the
		range 0 to 65535 inclusive.
	"""
	def __init__(self, isServer: bool, address: (str, int)) -> None:
		socket.setdefaulttimeout(NETWORK_TIMEOUT)
		if not 0 <= address[1] <= 65535:
			raise PiNetError("Invalid port.")
		self.__address = address
		self.__isServer = isServer
		self.__responses = {}
		self.__messages = []
		self.__dataObjs = []
		self.__conn = {"thread": None, "conn": None, "host": None,
			"isRunning": False}

	""" Registers a NetData object with the PiNet instance so it may be used to
		service requests from peers. Can only be called when the connection is not
		running.

	obj - The NetData object to be registered.

	Raises PiNetError 'Cannot register data objects once the connection is active'
		when called on an instance with an active connection.
	"""
	def registerNetDataObj(self, obj: NetData) -> None:
		if not self.__conn["isRunning"]:
			self.__dataObjs.append(obj)
		else:
			log.warning("Cannot register data objects once the connection " \
				"is active.")
			raise PiNetError("Cannot register data objects once the connection " \
				"is active.")

	""" Starts the process by which the PiNet instance will seek a network
		connection with other computers. Note that registerNetDataObj may not be
		called once the connection is running.

	Raises PiNetError 'Unable to connect to server.' if a connection with the
		specified server cannot be established.
	Raises PiNetError 'Socket connection already running.' if the socket is
		already connected.
	"""
	def start(self) -> None:
		if self.__conn["thread"] == None:
			if self.__isServer:
				self.__clients = {}
				self.__conn["isRunning"] = True
				self.__conn["thread"] = threading.Thread(target=self.__acceptClients)
				self.__conn["conn"] = socket.socket()
				self.__conn["conn"].bind(self.__address)
				self.__conn["thread"].start()
				self.__conn["conn"].listen()
				log.info("Server listening for clients on {0}.".format(self.__address))
			else:
				try:
					self.__conn["conn"] = socket.socket()
					self.__conn["conn"].connect(self.__address)
				except:
					log.error("Unable to connect to server at {0}.".format(self.__address))
					raise PiNetError("Unable to connect to server.")
				else:
					self.__conn["isRunning"] = True
					self.__conn["thread"] = threading.Thread(target=self.__tendServer)
					self.__conn["thread"].start()
					log.info("Client connected to server at {0}.".format(self.__address))
		else:
			log.error("Socket connection already running")
			raise PiNetError("Socket connection already running.")		

	""" Returns a boolean indicating whether or not the connection is active.
	"""
	def isRunning() -> bool:
		return self.__conn["isRunning"]


	""" Updates the address of the connection. Can only be called if isRunning()
		is False.

	Raises PiNetError 'Cannot change the connection address while the connection
		is active' if called when isRunning() is True.
	"""
	def setAddress(address: (str, int)) -> None:
		if self.__conn["isRunning"]:
			log.warning("Cannot change the connection address while the connection " \
				"is active")
			raise PiNetError("Cannot change the connection address while the " \
				"connection is active")
		else:
			self.__address = address

	""" Called asynchronously in server instances to constantly listen for remote
	clients attempting to connect.
	"""
	def __acceptClients(self) -> None:
		while self.__conn["isRunning"]:
			conn = None
			host = None
			try:
				conn, host = self.__conn["conn"].accept()
			except:
				# This will be caught often as it's expected to time out continually
				pass
			else:
				self.__clients[str(host[1])] = {"thread": None, "conn": conn,
					"isRunning": True, "host": host}
				thread = threading.Thread(target=self.__tendClient, 
					args=[self.__clients[str(host[1])]])
				self.__clients[str(host[1])]["thread"] = thread
				thread.start()
				log.info("Client connected from {0}.".format(host))

	""" Called by an asynchronous thread servicing a connection to receive
		messaged from its peer and address them accordingly.

	peer - The connection-specification dictionary for the client to be
		serviced.
	"""
	def __handleMsg(self, peer: dict) -> None:
		request = self.__recvMsg(peer)
		if message == "":
			return
		elif message == "closing":
			if self.__isServer:
				peer["isRunning"] = False
				peer["conn"].close()
				log.info("Client connection closed by peer from {0}.".format(peer["host"]))
				self.__clients.pop(str(peer["host"][1]))
			else:
				log.info("Connection closed by server from {0}".format(self.__address))
				self.__conn["isRunning"] = False
			return
		elif "responseKey" in message:
			self.__responses[request["responseKey"]] = message
		elif "msg" in message:
			self.__messages.append(request)
		else:
			response = {}
			if "query" in message and message["query"][0] == "total_data":
				response = self.__makeTotalNetDataPayload()
			elif "query" in message:
				for i in self.__dataObjs:
					if i.name in message["query"]:
						response[i.name] = i.value
			response["responseKey"] = message["requestKey"]
			if len(response) > 0:
				payload = json.dumps(response, separators=(',', ':'))
				st = threading.Thread(target=self.__send, args=(peer, payload))
				st.start()

	""" Called asynchronously in server instances to service a connection opened
		with a client.

	peer - The connection-specification dictionary for the client to be
		serviced.
	"""
	def __tendClient(self, peer: dict) -> None:
		while peer["isRunning"]:
			self.__handleMsg(peer)

	""" Called asynchronously in client instances to service a connection opened
		with a server.

	peer - The connection-specification dictionary for the client to be
		serviced.	
	"""
	def __tendServer(self) -> None:
		while self.__conn["isRunning"]:
			self.__handleMsg(self.__conn)

	""" Called by an asynchronous thread to receive messages from a specified
		peer.

	peer - The connection-specification dictionary of the peer the
		message should be received from.
	"""
	def __recvMsg(self, peer: dict) -> dict:
		request = ""
		while True:
			data = None
			try:
				data = peer["conn"].recv(1024)
			except:
				pass
			if data == None:
				if len(request) > 0:
					return json.loads(request)
				else:
					return ""
			else:
				request = request + data.decode()

	""" Called asynchronously to send messages to a specified peer.

	peer - The connection-specification dictionary of the peer the message should
		be sent to.
	payload - A string containing the message to be sent.
	"""
	def __send(self, peer, payload: str) -> None:
		try:
			peer["conn"].sendall(payload.encode())
		except:
			peer["isRunning"] = False
			peer["conn"].close()
			peer["thread"].join()
			if self.__isServer:
				for host, client in self.__clients.items():
					if client == peer:
						log.error("Failed to send message to client at {0}, " \
							"closing socket.".format(peer["host"]))
						self.__clients.pop(host)
						break
			else:
				log.error("Failed to send message to server at {0}, " \
					"closing socket.".format(self.__address))
				self.__conn["thread"] = None

	""" Creates a JSON string of all NetData objects registered with the PiNet
		instance to satisfy a 'total_data' request made by a peer.
	"""
	def __makeTotalNetDataPayload(self) -> str:
		total_data = {}
		for var in self.__dataObjs:
			total_data[var.name] = var.value
		payload = {"total_data": total_data}
		return payload

	""" Makes a 'data_request' to a peer (who must be specified if called
		by a server instance). Returns an responseKey integer to retrieve the
		JSON returned by the peer with getResponse().

	names - A list of NetData names to be requested of the peer. If only
		'total_data', a response containing all of the NetData values maintained by
		the peer will be sent as obtained from ____makeTotalNetDataPayload().
	target - If the caller is a server, it is necessary to specify which client
		the outgoing request is to be sent to. An exception will be raised if target
		is its default value in this case.

	Raises PiNetError 'Parameter names must be a non-empty string.' when called
		with an empty names argument.
	Raises PiNetError 'Target not specified for the request' when the target
		parameter is not given when called by a server instance of PiNet.
	Raises PiNetError 'Specified target is not available.' when the client peer
		targeted by the operation is not connected.
	"""
	def poseQuery(self, names: List[str], target="") -> int:
		if len(name) == 0:
			raise PiNetError("Parameter names must be a non-empty string.")
			log.error("poseQuery() - Parameter names must be a non-empty string")
		requestKey = self.__registerResponse()
		query = {"requestKey": requestKey, "query": names}
		requestPayload = json.dumps(query, separators=(',', ':'))
		if self.__isServer:
			target = str(target)
			if target != "":
				if target in self.__clients and self.__clients[target]["isRunning"]:
					st = threading.Thread(target=self.__send, 
						args=(self.__clients[target], requestPayload))
					st.start()
				else:
					log.error("Specified target is not available.")
					raise PiNetError("Specified target is not available.")
			else:
				log.error("Target not specified for the request.")
				raise PiNetError("Target not specified for the request.")
		else:
			st = threading.Thread(target=self.__send, 
				args=(self.__conn, requestPayload))
			st.start()
		return requestKey

	""" Sends a message to a peer. Unlike poseQuery(), a response from the peer is
		not expected.

	msg = A string containing the message to be sent.
	target - If the caller is a server, it is necessary to specify which client
		the outgoing message is to be sent to. An exception will be raised if target
		is its default value in this case.
	desc - An optional string identifier for the recipient to differentiate
		messages of different purposes with.

	Raises PiNetError 'Target not specified for the message' when the target
		parameter is not given when called by a server instance of PiNet.
	Raises PiNetError 'Specified target is not available.' when the client peer
		targeted by the operation is not connected.
	"""
	def sendMsg(self, msg:str, desc="", target="") -> None:
		msgPayload = {"msg": msg, "type": desc}
		msgPayload = json.dumps(msgPayload , separators=(',', ':'))
		if self.__isServer:
			target = str(target)
			if target != "":
				if target in self.__clients and self.__clients[target]["isRunning"]:
					st = threading.Thread(target=self.__send, 
						args=(self.__clients[target], msgPayload))
					st.start()
				else:
					log.error("Specified target is not available.")
					raise PiNetError("Specified target is not available.")
			else:
				log.error("Target not specified for the message.")
				raise PiNetError("Target not specified for the message.")
		else:
			st = threading.Thread(target=self.__send, args=(self.__conn, msgPayload))
			st.start()

	""" Returns the most recent message received by a peer as a dictionary of
		strings.
	"""
	def getMsg(self) -> Dict[str, str]:
		if len(self.__messages) > 0:
			return self.__messages.pop(0)

	""" Returns a list of all pending messages received by peers as dictionaries
		of strings.
	"""
	def getMsgs(self) -> List[Dict[str, str]]:
		msgs = self.__messages.copy()
		self.__messages.clear()
		return msgs

	""" Called by a method dispatching a request to obtain a responseKey so that
		any data returned in a response may be obtained after with getResponse().

	Raises PiNetError "Fatal, maximum number of pending responses exceeded." when
		there are 256 responses already registered and waiting collection.
		Intentionally left uncaught as under correct implementation and normal
		operation should never occur.
	"""
	def __registerResponse(self) -> int:
		if len(self.__responses) == 256:
			log.critical("Fatal, maximum number of pending responses exceeded.")
			raise PiNetError("Fatal, maximum number of pending responses exceeded.")
		key = random.randint(0, 255)
		while key in self.__responses:
			key = random.randint(0, 255)
		self.__responses[key] = ""
		return key

	""" Called by a thread after dispatching a request to a peer to obtain
		the returned JSON response. 

	key - The responseKey integer returned by the request dispatching function.
	"""
	def getResponse(self, key: int) -> Union[dict, None]:
		if key in self.__responses and self.__responses[key] != None:
			return self.__responses.pop(key)
		else:
			return None
		
	""" Returns a dictionary containing all pending responseKey response value
		pairs, flushing the internal storage.
	"""
	def getResponses(self) -> dict:
		responses = {i:r for (i,r) in self.__responses.items() if r != None}
		self.__responses = {i:r for (i,r) in self.__responses.items() if r == None}
		return responses

	""" Correctly terminates a connection with peers as soon as possible
		and kills all open threads.
	"""
	def stop(self) -> None:
		if self.__conn["isRunning"]:
			closePayload = json.dumps("closing", separators=(',', ':')).encode()
			self.__conn["isRunning"] = False
			self.__conn["thread"].join()
			if self.__isServer:
				log.info("Closing client listener at {0}.".format(self.__address))
				for host, client in self.__clients.items():
					client["isRunning"] = False
					client["thread"].join()
					try:
						client["conn"].sendall(closePayload)
					except:
						pass
					finally:
						time.sleep(NETWORK_TIMEOUT)
					client["conn"].close()
					log.info("Closing client connection at {0}.".format(client["host"]))
			else:
				log.info("Closing server connection at {0}.".format(self.__address))
				try:
					self.__conn["conn"].sendall(closePayload)
				except:
					pass
				finally:
					time.sleep(NETWORK_TIMEOUT)
			self.__conn["conn"].close()
			self.__responses = {}
			self.__messages	= []

	""" Returns a list of all the connected client's host names. The names are
		used to target peers when performing operations as a server instance.
		Peers reflected in this list are available to data transmission or
		reception.

	Raises PiNetError "Invalid operation for clients." when called from a client
		instance.
	"""
	def getConnected(self) -> List[str]:
		if self.__isServer:
			return list(self.__clients.keys())
		else:
			log.warning("Clients should not call getConnected().")
			raise PiNetError("Invalid operation for clients.")


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
				if key % 2 == 0:
					payload = payload + data.to_bytes(2, "big")
				else:
					log.error("Integer data keys must be even.")
					raise ArduinoNetError("Integer data keys must be even.")
			elif type(data) == float:
				if key % 2 == 1:
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
