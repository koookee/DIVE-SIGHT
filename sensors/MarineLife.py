import time
from threading import Thread
import serial
import sys

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyS0', BAUD_RATE, timeout=1)

class MarineLifeThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.warning = False
        self.msg = ""
        
    def run(self):
        while True:
            if "shark" in self.receive_msg():
                self.warning = True
            else:
                self.warning = False
            time.sleep(1)

    def receive_msg(self):
        self.msg = ser.readline()
        return self.msg.decode("utf-8")
        