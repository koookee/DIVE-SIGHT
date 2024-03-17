import time
from threading import Thread
from Accelerometer import AccelerometerThread
from HeartRate import HeartRateThread
from OxygenLevels import OxygenThread

accelerometer = AccelerometerThread()
heart_rate = HeartRateThread()
oxygen_levels = OxygenThread()

accelerometer.start()
heart_rate.start()
oxygen_levels.start()

while True:

    # Pseudocode ...
    # warningArr = []
    # if getOxWarning:
    #     warningArr.append(o2WarningMsg)
    # if getHeartWarning:
    #     warningArr.append(heartWarningMsg)
    # if getAccWarning:
    #     warningArr.append(accWarningMsg)
    # if getSharkWarning
    #     warningArr.append(sharkWarningMsg)

    # numOfWarnings = len(warningArr)

    # if numOfWarnings > 0:
    #     lcdDisplay.print(f"{numOfWarnings} warning(s): {warningArr}")
    # else:
    #     lcdDisplay.print(sensor data)