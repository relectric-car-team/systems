from typing import Tuple
from controller import *
from controllerdata import *
from controllers import *

class Systems():
  
  """ Creates and initializes all of the controllers
  """
  def __init__(self):
    self.controllers = [];
    self.controllers.append(MotorController())
    self.controllers.append(BatteryController())
    self.controllers.append(ClimateController())
    self.controllers.append(SensorController())
    self.controllers.append(BackupController())

  """ Finds and returns the value of the specified variable in a certain controller
  """
  def get(name: str) -> any:
    for i in controllers:
      value = controllers[i].getVariable(controllers[i], name)
      if value is not None:
        return value
    return None

  """ Finds and sets the value of the specified variable in a certain controller
  """
  def set(name: str, value: any) -> None:
    for i in controllers:
      if name in controllers[i].variables:
        controllers[i].setVariable(name, value) 
        return

  """ Calls the action specified by a controller with the provided arguments
  """
  def sendAction(name: str, args: Tuple[any]) -> None:
    for i in controllers:
      if name in controllers[i].actions:
        controllers[i].performAction(controllers[i], name, args)
        return
        
  """ Shuts the controllers down
  """
  def shutdown(self) -> None:
    for i in controllers:
      controllers[i].shutdown()
  
