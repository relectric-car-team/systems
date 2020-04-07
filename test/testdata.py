class TestData():

# change test data file
CONST_FILE_NAME = "testdata.csv"
  def loadData(self) -> None:
    file = open(CONST_FILE_NAME, "r")

  def update(self) -> None:
    file = open(CONST_FILE_NAME, "w")
    

  def get(self, name: str) -> None:
    pass