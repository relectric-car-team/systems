from typing import Tuple
from controller import *
from controllerdata import *
from controllers import *
from net import *
from networkmanager import NetworkManager

""" The Systems class is the main object that encapsulates the program for the
  electric car central systems. It consists of a set of 'controller' modules
  that each contribute separate functions to control and manage different
  sub-systems in the car (battery, motor, climate control, etc). In addition,
  this class owns an instance of NetworkManager, an object containing instances
  of all the necessary abstracted networking interfaces needed to communicate
  with the aforementioned sub-systems. The NetworkManager is passed to each
  controller upon initialization.
"""
class Systems():
  
  """ Creates and initializes the network manager and all of the controllers.
  """
  def __init__(self):
    self.controllers = []
    self.networkManager = NetworkManager([])
    self.controllers.append(MotorController(self.networkManager))
    self.controllers.append(BatteryController(self.networkManager))
    self.controllers.append(ClimateController(self.networkManager))
    self.controllers.append(SensorController(self.networkManager))
    self.controllers.append(BackupController(self.networkManager))

  """ Finds and returns the value of the specified variable that belongs to one
    of the controllers.
  
      name - A string to identify the variable.
  """
  def get(name: str) -> any:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        return self.controllers[i].getVariable(self.controllers[i], name)
    return None

  """ Finds and sets the value of the specified variable that belongs to one of
    the controllers.
  
      name - A string to identify the variable.
      value - New value for the specified variable.
  """
  def set(name: str, value: any) -> None:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        self.controllers[i].setVariable(name, value) 
        return

  """ Calls the action specified by a controller with the provided arguments.
  
      name - A string to identify the action.
      args - Tuple of arguments to pass to the function.
  """
  def sendAction(name: str, args: Tuple[any]) -> None:
    for i in self.controllers:
      if name in self.controllers[i].actions:
        self.controllers[i].performAction(self.controllers[i], name, args)
        return
        
  """ Shuts the controllers down.
  """
  def shutdown(self) -> None:
    for i in self.controllers:
      self.controllers[i].shutdown()

# Main module entry point.
if __name__ == "__main__":
  systems = Systems()
