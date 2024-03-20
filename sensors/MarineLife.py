import time
from threading import Thread
import serial
import sys

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyS0', BAUD_RATE)

class MarineLifeThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.warning = False
        self.msg = ""
        
    def run(self):
        while True:
            receive_msg()

    def receive_msg():
        self.msg = ser.readline()
        print(self.msg)