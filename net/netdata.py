""" Encapsulates data to facilitate ownership by local software and usage for
	data requests by peers in the PiNet and ArduinoNet classes.

As Python python does not have C/C++ style pointers, it is necessary to pass
	variables by reference in order for the caller of this module to maintain
	ownership of them. The NetData class is to be instantiated by the caller and
	provided to instances of PiNet or ArduinoNet with the RegisterNetDataObj()
	methods.
"""
class NetData():
	""" Constructs and instance of the NetData class.

	name - A string representing the data housed by the object. Peers will
		refer to specific variables by this name.
	value - The object to be held by this instance. value should only be a basic
		data type available in Python.
	"""
	def __init__(self, name: str, value: any) -> None:
		self.name = name
		self.value = value
