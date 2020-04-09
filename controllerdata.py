from enum import Enum

class VariableAccess(Enum):
  READ = 0
  WRITE = 1
  READWRITE = 2

class ControllerData():
  def __init__(self, name = None, value = None, access = VariableAccess.READ):
    self.name = name
    self.value = value
    self.access = access