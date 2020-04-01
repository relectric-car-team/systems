from enum import Enum

class VariableAccess(Enum):
  READ = 0
  WRITE = 1
  READWRITE = 2

class ControllerData():
  pass