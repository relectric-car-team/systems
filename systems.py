from typing import Tuple

class Systems():
  def __init__(self):
    pass

  def registerVariable(self, name: str, value: any, variableType: any) -> str:
    pass

  def setVariable(self, name: str, value: any) -> None:
    pass

  def registerAction(self, name: str, callback: any) -> None:
    pass

  def performAction(self, name: str, args: Tuple[any]) -> None:
    pass

  def shutdown(self):
    pass