import pandas as pd  # pip install pandas

# Constants
CONST_FILE_NAME = "testdata.csv"
col_list = []

df = pd.read_csv(CONST_FILE_NAME, skiprows = 1) #read the csv file, skipping the headers

class TestData:
    """ TestData accesses the file of mock data to send to other classes in
    place of any engine, battery, sensor, etc. data.
    """
    
    def __init__(self):
        """ Initializes TestData variables which are all potential data that
        could be	sent from other functions of the vehicle. Time is set to 0
        to begin.
        """
        pd.read_csv(CONST_FILE_NAME, nrows = 1).col_list.tolist() #read the headers of the controller and store into a list
        self.time = 0

    def update(self) -> None:
        """ Increment time which is used to keep track of which index from
        the data arrays to access.
        """
        self.time += 1

    def get(self, name: str) -> any:
        """ Return any requested data that is passed as an argument. Will
        return the current data as dictated by current time value.
        """

        for i in col_list: #loop through header names
            if name == i:
                return df[i][self.time] #if the argument name matches the header, return the value of the argument at given time
