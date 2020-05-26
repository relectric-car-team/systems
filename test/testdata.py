import pandas as pd  # pip install pandas

# Constants
CONST_FILE_NAME = "testdata.csv"
col_list = ["speed", "voltage", "RPM", "temperature"]


class TestData:
    """ TestData accesses the file of mock data to send to other classes in
    place of any engine, battery, sensor, etc. data.
    """

    def __init__(self):
        """ Initializes TestData variables which are all potential data that
        could be	sent from other functions of the vehicle. Time is set to 0
        to begin.
        """
        file = pd.read_csv(CONST_FILE_NAME, usecols=col_list, sep=",")
        self.speed = file["speed"]
        self.voltage = file["voltage"]
        self.RPM = file["RPM"]
        self.temperature = file["temperature"]
        self.time = 0

    def update(self) -> None:
        """ Increment time which is used to keep track of which index from
        the data arrays to access.
        """
        self.time += 1

    def get(self, name: str) -> None:
        """ Return any requested data that is passed as an argument. Will
        return the current data as dictated by current time value.
        """
        if name == "speed":
            return self.speed[self.time]
        elif name == "voltage":
            return self.voltage[self.time]
        elif name == "RPM":
            return self.RPM[self.time]
        elif name == "temperature":
            return self.temperature[self.time]
