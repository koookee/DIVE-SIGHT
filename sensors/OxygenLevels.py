import time
from time import sleep
import argparse
from max30102 import HeartRateMonitor
from threading import Thread

class OxygenThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.hrm = HeartRateMonitor(False, True)
        self.send_sos = False
        self.start_time = time.time()
        self.o2 = 0
        
    def run(self):
        while True:
            self.o2 = round(self.hrm.get_oxygen(), 2)
            self.checkForSOS()

    def checkForSOS(self):
        if ((self.o2 > 100) or (self.o2 < 93)):
            if (abs(self.start_time - time.time()) > 30):
                self.send_sos = True
        else:
            self.start_time = time.time()
            self.send_sos = False
    
    '''
    # checking outputs
    print(f"O2: {o2}")
    print(abs(start_time - time.time()))
    print(f"sos: {send_sos}\n")
    '''