from typing import Tuple
from controller import *
from controllerdata import *
from controllers import *

class Systems():
  
  """ Creates and initializes all of the controllers
  """
  def __init__(self):
    self.controllers = []
    self.controllers.append(MotorController())
    self.controllers.append(BatteryController())
    self.controllers.append(ClimateController())
    self.controllers.append(SensorController())
    self.controllers.append(BackupController())

  """ Finds and returns the value of the specified variable in a certain controller
  
      name - Name of the variable
  """
  def get(name: str) -> any:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        value = self.controllers[i].getVariable(self.controllers[i], name)
        return value
    return None

  """ Finds and sets the value of the specified variable in a certain controller
  
      name - Name of the variable
      value - New value for the specified variable
  """
  def set(name: str, value: any) -> None:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        self.controllers[i].setVariable(name, value) 
        return

  """ Calls the action specified by a controller with the provided arguments
  
      name - Name of the variable
      args - Tuple of arguments to padd to the function
  """
  def sendAction(name: str, args: Tuple[any]) -> None:
    for i in self.controllers:
      if name in self.controllers[i].actions:
        self.controllers[i].performAction(self.controllers[i], name, args)
        return
        
  """ Shuts the controllers down
  """
  def shutdown(self) -> None:
    for i in self.controllers:
      self.controllers[i].shutdown()
  
if __name__ == "__main__":
  systems = Systems()