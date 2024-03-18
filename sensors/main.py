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
    warnings = []
    if accelerometer.send_sos:
        warnings.append("falling unconscious")
    if heart_rate.send_sos:
        warnings.append("irregular heart rate")
    if oxygen_levels.send_sos:
        warnings.append("irregular oxygen levels")
    
    # if getSharkWarning
    #     warnings.append(sharkWarningMsg)

    warnings_str = ", ".join(warnings)

    if len(warnings) > 0:
        print(f"{len(warnings)} warning(s): {warnings_str}")
        # lcdDisplay.print(f"{len(warnings)} warning(s): {warningArr}")
    # else:
    #     lcdDisplay.print(sensor data)