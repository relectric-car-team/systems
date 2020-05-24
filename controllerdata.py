from enum import Enum


class VariableAccess(Enum):
    """ Enumeration of the different access states a ControllerData instance can
    hold.
    """
    READ = 0
    WRITE = 1
    READWRITE = 2


class ControllerData:
    """ A simple class to encapsulate the data variables shared between the
    controllers and Systems.
    """

    def __init__(self, name: str, value=None, access=VariableAccess.READ):
        """ Initializes the ControllerData object with the variable's name, a
        default	value, and the access state.
        """
        self.name = name
        self.value = value
        self.access = access
