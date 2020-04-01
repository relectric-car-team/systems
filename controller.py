from typing import Tuple

class Controller():
  def registerVariable(self, name: str, value: any, type: any) -> None:
    pass

  def setVariable(self, name: str, callback: any) -> None:
    pass

  def registerAction(self, name: str, args: Tuple[any]) -> None:
    pass
  
  def performAction(self, name: str, args: Tuple[any]) -> None:
    pass
  
  def shutdown(self) -> None:
    pass