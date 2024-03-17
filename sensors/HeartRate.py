import time
from time import sleep
import argparse
from max30102 import HeartRateMonitor
from threading import Thread

class HeartRateThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.hrm = HeartRateMonitor(False, True)
        self.send_sos = False
        self.start_time = time.time()
        
    def run(self):
        while True:
            self.heart_rate = round(self.hrm.get_heart_rate(), 2)
            self.checkForSOS()

    def checkForSOS(self):
        if ((self.heart_rate > 120) or (self.heart_rate < 40)):
            if (abs(self.start_time - time.time()) > 30):
                self.send_sos = True
        else:
            self.start_time = time.time()
            self.send_sos = False
    
    '''
    # checking outputs
    print(f"Heart Rate: {heart_rate}")
    print(abs(start_time - time.time()))
    print(f"sos: {send_sos}\n")
    '''