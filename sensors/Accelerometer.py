import time
from time import sleep
from mpu6050 import mpu6050
from threading import Thread

class AccelerometerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.accelerometer = mpu6050(0x68)
        self.pval_x = 0
        self.pval_y = 0
        self.pval_z = 0
        self.send_sos = False
        self.start_time = time.time()
        self.val_x = 0
        self.val_y = 0
        self.val_z = 0

    def run(self):
        while True:
            m = self.accelerometer.get_accel_data()
            
            self.val_x = m['x']
            self.val_y = m['y']
            self.val_z = m['z']
            
            self.checkForSOS()
                    
            self.pval_x = self.val_x
            self.pval_y = self.val_y
            self.pval_z = self.val_z

    def checkForSOS(self):
        if (((abs(self.val_x - self.pval_x)) < 5 ) and ((abs(self.val_y - self.pval_y)) < 5 ) and ((abs(self.val_z - self.pval_z)) < 5 )):
            if (abs(self.start_time - time.time()) > 30):
                self.send_sos = True
        else:
            self.start_time = time.time()
            self.send_sos = False

    '''
    # checking outputs
    print(abs(start_time - time.time()))
    print(f"warning: {display_warning}")
    print(f"sos: {send_sos}\n")
    sleep(2)
    '''
    