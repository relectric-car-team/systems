import pandas as pd  # pip install pandas
import sys

class TestData:
    """ TestData accesses the file of mock data to send to other classes in
    place of any engine, battery, sensor, etc. data.
    """
    
    def __init__(self, file_path):
        """ Initializes TestData variables which are all potential data that
        could be	sent from other functions of the vehicle. Time is set to 0
        to begin.
        """
        self.file = pd.read_csv(file_path)
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

        return self.file[name][self.time]
