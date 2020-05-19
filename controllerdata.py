from enum import Enum

""" Enumeration of the different access states a ControllerData instance can
	hold.
"""
class VariableAccess(Enum):
	READ = 0
	WRITE = 1
	READWRITE = 2

""" A simple class to encapsulate the data variables shared between the
	controllers and Systems.
"""
class ControllerData():
	""" Initializes the ControllerData object with the variable's name, a
	default	value, and the access state.
	"""
	def __init__(self, name=None, value=None, access=VariableAccess.READ):
		self.name = name
		self.value = value
		self.access = access
