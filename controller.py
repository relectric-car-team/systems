from typing import Tuple, Optional, Callable
from controllerdata import ControllerData, VariableAccess
from abc import ABC
from networkmanager import NetworkManager
from controllererror import ControllerError


class Controller(ABC):
    """ Controller is an abstract base class that all controller classes
    should inherit from. It provides a set of base functionality, and some
    callbacks to be overridden by the child class.
    """

    def __init__(self, network_manager: NetworkManager):
        """ Initializes the variables and actions dictionaries for the
        Controller.
        """
        self.networkManager = network_manager
        self.__variables = {}
        self.__actions = {}

    def __register_variable(self, name: str, value: any,
                            access: VariableAccess =
                            VariableAccess.READWRITE) -> None:
        """ Registers a new variable for the controller.

        name - String identifier of the variable to register.
        value - The default value of the variable.
        access - A VariableAccess to assign the access state of the variable.
        """
        if name in self.__variables:
            raise Exception(
                "Cannot register two variables with the same name '",
                name, "' in: ", type(self).__name__)
        self.__variables[name] = ControllerData(name=name, value=value,
                                                access=access)

    def set_variable(self, name: str, value: any, bypass: bool = True) -> None:
        """ Sets the value of an existing variable.

        name - String identifier of the variable to change.
        value - New value for the variable.
        bypass - If True, bypasses read/write access restrictions.
        """
        if name not in self.__variables:
            raise ControllerError("Variable '", name,
                                  "' does not exist on type ",
                                  type(self).__name__)
        if not bypass:
            if self.__variables[value].access == VariableAccess.READ:
                raise ControllerError("Variable '", name,
                                      "' is read-only, cannot write to it")
        self.__variables[name].value = value

    def has_variable(self, name: str) -> bool:
        """ Returns whether the controller has registered a variable with given
        name.

        name - String identifier for the variable to check for.
        """
        return name in self.__variables

    def has_action(self, name: str) -> bool:
        """ Returns whether the controller has registered an action with
        given name.

        name - String identifier for the action to check for.
        """
        return name in self.__actions

    def get_variable(self, name: str, bypass: bool = False) -> any:
        """ Returns the value of a variable

        name - Name of the variable to look for
        bypass - Bypass read/write access restrictions
        """
        if name not in self.__variables:
            raise ControllerError("Variable '", name,
                                  "' does not exist on type ",
                                  type(self).__name__)
        if not bypass:
            if self.__variables[name].access == VariableAccess.WRITE:
                raise ControllerError("Variable '", name,
                                      "' is write-only, cannot read from it")
        return self.__variables[name].value

    def __register_action(self, name: str, callback: Callable) -> None:
        """ Registers a new action function

        name - String identifier of the action to register.
        callback - Callback function for when the action is called.
        """
        if name not in self.__actions:
            raise ControllerError(
                "Cannot register two actions with the same name '",
                name, "' in: ", type(self).__name__)
        if not callable(callback):
            raise ControllerError("Registered action must be a function: ",
                                  name)
        self.__actions[name] = callback

    def perform_action(self, name: str, args: Optional[Tuple[any]]) -> None:
        """ Performs a given action, with given arguments.

        name - String identifier of the action to perform.
        args - Tuple of arguments to pass to the function.
        """
        if name not in self.__actions:
            raise ControllerError("Actions with the name does not exist '",
                                  name,
                                  "' in: ", type(self).__name__)
        if not callable(self.__actions[name]):
            raise ControllerError("Registered action must be a function: ",
                                  name)
        self.__actions[name](args=args)

    def shutdown(self) -> None:
        """ Safely terminates the controller. To be overridden by classes
        implementing Controller if needed.
        """
        pass
