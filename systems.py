from typing import Tuple
from controller import *
from controllerdata import *
from controllers import *

class Systems():
  
  # Creates and initializes all of the controllers
  def __init__(self):
    self.controllers = [];
    controllers[0] = MotorController()
    controllers[1] = BatteryController()
    controllers[2] = ClimateController()
    controllers[3] = SensorController()
    controllers[4] = BackupController()

  # Finds and returns the value of the specified variable in a certain controller
  def get(name: str) -> any:
    for i in controllers:
      value = controllers[i].getVariable(controllers[i], name)
      return value

  # Finds and sets the value of the specified variable in a certain controller
  def set(name: str, value: any) -> None:
    for i in controllers:
      if name in controllers[i].variables:
        controllers[i].setVariable(name, value)  

  # Calls the action specified by a controller with the provided arguments
  def sendAction(name: str, args: Tuple[any]) -> None:
    for i in controllers:
      if name in controllers[i].actions:
        controllers[i].performAction(controllers[i], name, args)
        
  # Shuts the controllers down
  def shutdown(self) -> None:
    for i in controllers:
      controllers[i].shutdown()
  
