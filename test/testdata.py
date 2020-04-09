import pandas as pd

CONST_FILE_NAME = "testdata.csv"
col_list = ["speed", "voltage", "RPM", "temperature"]


class TestData():
    def __init__(self, speed, voltage, RPM, temperature, time):
        self.speed = []
        self.voltage = []
        self.RPM = []
        self.temperature = []
        self.time = 0

    def loadData(self) -> None:
        file = pd.read_csv(CONST_FILE_NAME, usecols=col_list)
        self.speed = file["speed"]
        self.voltage = file["voltage"]
        self.RPM = file["RPM"]
        self.temperature = file["temperature"]

    def update(self) -> None:
        file = open(CONST_FILE_NAME, "w")
        #dont know what to update with to be continued...

    def get(self, name: str) -> None:
        if name == "speed":
            return self.speed[self.time]
        elif name == "voltage":
            return self.voltage[self.time]
        elif name == "RPM":
            return self.RPM[self.time]
        elif name == "temperature":
            return self.temperature[self.time]
        self.time = self.time + 1