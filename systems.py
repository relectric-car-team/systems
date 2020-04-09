from typing import Tuple
from controller import *
from controllerdata import *
from controllers import *

class Systems():
  
  def __init__(self):
    self.controllers = [];
    controllers[0] = MotorController
    controllers[1] = BatteryController
    controllers[2] = ClimateController
    controllers[3] = SensorController
    controllers[4] = BackupController

  def get(name: str) -> any:
    for i in controllers:
      if name in controllers[i].variables:
        return controllers[i].variables[name].value
    return null

  def set(name: str, value: any) -> None:
    for i in controllers:
      if name in controllers[i].variables:
        controllers[i].variables[name].value = value  

  def sendAction(name: str, args: Tuple[any]) -> None:
    for i in controllers:
      if name in controllers[i].actions:
        controllers[i].performAction(controllers[i], name, args)
        

  def shutdown(self) -> None:
    for i in controllers:
      controllers[i].shutdown()
  
