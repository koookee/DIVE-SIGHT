import time
from time import sleep
from mpu6050 import mpu6050

accelerometer = mpu6050(0x68)
    
pval_x = 0
pval_y = 0
pval_z = 0

display_warning = False
send_sos = False

start_time = time.time()

while True: 
    m = accelerometer.get_accel_data()
    
    val_x = m['x']
    val_y = m['y']
    val_z = m['z']
    
    if (((abs(val_x - pval_x)) < 5 ) and ((abs(val_y - pval_y)) < 5 ) and ((abs(val_z - pval_z)) < 5 )):
        if (abs(start_time - time.time()) > 30):
            send_sos = True
            display_warning = False
        elif (abs(start_time - time.time()) > 15):
            display_warning = True
    else:
        start_time = time.time()
        send_sos = False
        display_warning = False
            
    pval_x = val_x
    pval_y = val_y
    pval_z = val_z
    
    '''
    # checking outputs
    print(abs(start_time - time.time()))
    print(f"warning: {display_warning}")
    print(f"sos: {send_sos}\n")
    sleep(2)
    '''
    