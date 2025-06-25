import sys
import time
from networktables import NetworkTables

shouldCheckConnection = True
teamNumber = input("Please enter the team number, or NA for GUI testing only: ")
ip = "127.0.0.1"
if teamNumber == "NA":
    shouldCheckConnection = False
else:
    match (len(teamNumber)):
        case 4:
            ip = "10." + teamNumber[0:2] + "." + teamNumber[2:4] + ".2"
            print(ip)
        case _:
            print("No support added yet for numbers less than 4 digits, sorry!")

    NetworkTables.initialize(server="127.0.0.1")  # localhost
    data = NetworkTables.getTable("SmartDashboard")
    time.sleep(1)  # Time to connect fully
    if data.getNumber("Reef Side", -1) != -1:
        print("CONNECTED: SIMULATOR")
    else:
        NetworkTables.initialize(server=ip)
        data = NetworkTables.getTable("SmartDashboard")
        time.sleep(1)  # Time to connect fully
        if data.getNumber("Reef Side", -1) == -1:
            if shouldCheckConnection:
                print("IMPORTANT: COULD NOT CONNECT/RETRIVE VALUES")
                print("Error: Could not connect to robot")
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
