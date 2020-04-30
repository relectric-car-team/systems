#Imports
import pandas as pd

# constants
CONST_FILE_NAME = "testdata.csv"
col_list = ["speed", "voltage", "RPM", "temperature"]


""" TestData accesses the file of mock data to send to other classes in place of any 
        engine, battery, sensor, etc. data.
"""

class TestData():
    """ Initizalizes TestData variables which are all potential data that could be sent
            from other functions of the vehicle. Time is set to 0 to begin.
    """
    def __init__(self, speed, voltage, RPM, temperature, time):
        self.speed = []
        self.voltage = []
        self.RPM = []
        self.temperature = []
        self.time = 0

    """ Reads data from file set in constants and places all data in arrays. Each column
            is an array and each entry is an element.
    """
    def loadData(self) -> None:
        file = pd.read_csv(CONST_FILE_NAME, usecols=col_list)
        self.speed = file["speed"]
        self.voltage = file["voltage"]
        self.RPM = file["RPM"]
        self.temperature = file["temperature"]

    """ Increment time which is used to keep track of which index from the data arrays to access.
    """
    def update(self) -> None:
        self.time = self.time + 1

    """ Return any requested data that is passed as an argument. Will return the current data
            as dictated by current time value.
    """
    def get(self, name: str) -> None:
        if name == "speed":
            return self.speed[self.time]
        elif name == "voltage":
            return self.voltage[self.time]
        elif name == "RPM":
            return self.RPM[self.time]
        elif name == "temperature":
            return self.temperature[self.time]
