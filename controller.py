from typing import Tuple, Optional
from controllerdata import ControllerData, VariableAccess
from abc import ABC

class Controller(ABC):
  def __init__(self):
    self.variables = {}
    self.actions = {}

  def registerVariable(self, name: str, value: any, access: VariableAccess) -> None:
    if name in self.variables:
      raise Exception("Cannot register two variables with the same name '", name, "' in: ", type(self).__name__)
    
    self.variables[name] = ControllerData(name=name, value=value, access=access)

  def setVariable(self, name: str, value: any) -> None:
    if not name in self.variables:
      raise Exception("Variable '", name, "' does not exist on type ", type(self).__name__)
    
    if self.variables[value].access == VariableAccess.READ:
      raise Exception("Variable '", name, "' is readonly, cannot write to it!")

    self.variables[name].value = value
  
  def getVariable(self, name: str) -> any:
    if not name in self.variables:
      raise Exception("Variable '", name, "' does not exist on type ", type(self).__name__)
    
    if self.variables[name].access == VariableAccess.WRITE:
      raise Exception("Variable '", name, "' is writeonly, cannot read from it!")
    
    return self.variables[name].value

  def registerAction(self, name: str, callback: any) -> None:
    if not name in self.actions:
      raise Exception("Cannot register two actions with the same name '", name, "' in: ", type(self).__name__)
    
    if not callable(callback):
      raise Exception("Registered action must be a function: ", name)
    
    self.actions[name] = callback
  
  def performAction(self, name: str, args: Optional[Tuple[any]]) -> None:
    if not name in self.actions:
      raise Exception("Actions with the name does not exist '", name, "' in: ", type(self).__name__)
    
    if not callable(self.actions[name]):
      raise Exception("Registered action must be a function: ", name)

    self.actions[name](args=args)
  
  def shutdown(self) -> None:
    pass