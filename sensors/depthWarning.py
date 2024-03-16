import time
from time import sleep
from bmp280 import BMP280

bmp = BMP280()

send_sos = False

start_time = time.time()

def convert_to_depth(p):
    return ((10 * (p * 0.000987)) - 10)

while True:
    start_depth_time = time.time()
    depth = convert_to_depth(bmp.get_pressure())
    
    sleep(5)
    
    rate_of_change = ((depth - convert_to_depth(bmp.get_pressure())) / (time.time() - start_depth_time))
    if (rate_of_change > (0.3)):
        if (abs(start_time - time.time()) > 30):
            send_sos = True

    else:
        start_time = time.time()
        send_sos = False
    
    '''
    # checking outputs
    print(abs(start_time - time.time()))
    print(f"sos: {send_sos}\n")
    print(f"roc: {rate_of_change}\n")
    sleep(2)
    '''
    