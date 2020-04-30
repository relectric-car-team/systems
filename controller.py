from typing import Tuple, Optional
from controllerdata import ControllerData, VariableAccess
from abc import ABC

""" Controller is an abstract base class that all controller classes should inherit from

It provides a set of base functionality, and some callbacks to be overridden by the child class
"""
class Controller(ABC):
  """ Initializes the variables and actions dictionaries for the Controller
  """
  def __init__(self, networkManager: Optional[any] = None):
    self.networkManager = networkManager
    self.variables = {}
    self.actions = {}

  """ Registers a new variable for the controller

      name - Name of the variable to register
      value - The default value of the variable
      access - The read/write access associated with this variable
  """
  def registerVariable(self, name: str, value: any, access: Optional[VariableAccess] = VariableAccess.READWRITE) -> None:
    if name in self.variables:
      raise Exception("Cannot register two variables with the same name '", name, "' in: ", type(self).__name__)
    
    self.variables[name] = ControllerData(name=name, value=value, access=access)

  """ Sets the value of an existing variable

      name - Variable name to set the value of
      value - New value for the variable
      bypass - Bypass read/write access restrictions
  """
  def setVariable(self, name: str, value: any, bypass: Optional[bool] = True) -> None:
    if not name in self.variables:
      raise Exception("Variable '", name, "' does not exist on type ", type(self).__name__)
    
    if not bypass:
      if self.variables[value].access == VariableAccess.READ:
        raise Exception("Variable '", name, "' is readonly, cannot write to it")

    self.variables[name].value = value
  
  """ Returns whether the controller has registered a variable with given name

      name - Name to check for
  """
  def hasVariable(self, name: str) -> bool:
    return name in self.variables
  
  """ Returns whether the controller has registered an action with given name

      name - Name to check for
  """
  def hasAction(self, name: str) -> bool:
    return name in self.actions
  
  """ Returns the value of a variable

      name - Name of the variable to look for
      bypass - Bypass read/write access restrictions
  """
  def getVariable(self, name: str, bypass: Optional[bool] = False) -> any:
    if not name in self.variables:
      raise Exception("Variable '", name, "' does not exist on type ", type(self).__name__)
    
    if not bypass:
      if self.variables[name].access == VariableAccess.WRITE:
        raise Exception("Variable '", name, "' is writeonly, cannot read from it")
    
    return self.variables[name].value

  """ Registers a new action function

      name - Name of the action
      callback - Callback function for when the action is called
  """
  def registerAction(self, name: str, callback: any) -> None:
    if not name in self.actions:
      raise Exception("Cannot register two actions with the same name '", name, "' in: ", type(self).__name__)
    
    if not callable(callback):
      raise Exception("Registered action must be a function: ", name)
    
    self.actions[name] = callback
  
  """ Performs a given action, with given arguments

      name - Name of the action to perform
      args - Tuple of arguments to pass to the function
  """
  def performAction(self, name: str, args: Optional[Tuple[any]]) -> None:
    if not name in self.actions:
      raise Exception("Actions with the name does not exist '", name, "' in: ", type(self).__name__)
    
    if not callable(self.actions[name]):
      raise Exception("Registered action must be a function: ", name)

    self.actions[name](args=args)
  
  """ Function called on controller shutdown

      To be overridden by classes implementing Controller if needed
  """
  def shutdown(self) -> None:
    pass