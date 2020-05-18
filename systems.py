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
    self.__controllers = []
    self.__networkManager = NetworkManager([])
    self.__controllers.append(MotorController(self.networkManager))
    self.__controllers.append(BatteryController(self.networkManager))
    self.__controllers.append(ClimateController(self.networkManager))
    self.__controllers.append(SensorController(self.networkManager))
    self.__controllers.append(BackupController(self.networkManager))
    self.__loop() # Note there is currently no end condition.

  """ Finds and returns the value of the specified variable that belongs to one
    of the controllers.
  
      name - A string to identify the variable.
  """
  def __getData(self, name: str) -> any:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        return self.controllers[i].getVariable(self.controllers[i], name)
    return None

  """ Finds and sets the value of the specified variable that belongs to one of
    the controllers.
  
      name - A string to identify the variable.
      value - New value for the specified variable.
  """
  def __setData(self, name: str, value: any) -> None:
    for i in self.controllers:
      if name in self.controllers[i].variables:
        self.controllers[i].setVariable(name, value) 
        return

  """ Calls the action specified by a controller with the provided arguments.
  
      name - A string to identify the action.
      args - Tuple of arguments to pass to the function.
  """
  def __sendAction(self, name: str, args: Tuple[any]) -> None:
    for i in self.controllers:
      if name in self.controllers[i].actions:
        self.controllers[i].performAction(self.controllers[i], name, args)
        return
        
  """ The main program loop for the systems computer. Listens for external
    requests and services them accordingly with the actions of controllers. The
    format of requests directed to the actions of controllers is a dictionary
    with the format {"type": ["action"|"get"|"set"], "name": ["name"], 
    ["args": []], ["value": any]}.
  """
  def __loop(self):
    while True:
      request = self.networkManager.getPiNet().getRequest()
      if request["type"] == "action":
        response = sendAction(request["name"], tuple(request["args"]))
      elif request["type"] == "get":
        try:
          response = get(request["name"])
        except:
          response = None
      elif request["type"] == "set":
        try:
          setData(request["name"], request["value"])
          response = True
        except:
          response = False
      self.networkManager.getPiNet().sendResponse(request["requestKey"],
        response, request["peer"])

  """ Shuts the controllers down.
  """
  def shutdown(self) -> None:
    for i in self.controllers:
      self.controllers[i].shutdown()

# Main module entry point.
if __name__ == "__main__":
  systems = Systems()
