import sys
import time
from networktables import NetworkTables


NetworkTables.initialize(server="127.0.0.1")
data = NetworkTables.getTable("SmartDashboard")
time.sleep(1)  # Time to connect fully
if data.getNumber("Reef Side", -1) != -1:
    print("CONNECTED: SIMULATOR")
else:
    NetworkTables.initialize(server="10.85.75.2")
    data = NetworkTables.getTable("SmartDashboard")
    time.sleep(1)  # Time to connect fully
    if data.getNumber("Reef Side", -1) == -1:
        print("IMPORTANT: COULD NOT CONNECT/RETRIVE VALUES")
        import error_window
    else:
        print("CONNECTED: REAL ROBOT")


def getNum(key):
    return data.getNumber(key, -1.0)


def setNum(key, value):
    # print(data.putNumber(key, value))
    data.putNumber(key, value)


def setBoolean(key, value):
    data.putBoolean(key, value)


def getBoolean(key):
    return data.getBoolean(key, False)
