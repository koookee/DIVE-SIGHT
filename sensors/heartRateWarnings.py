import time
from time import sleep
import argparse
from max30102 import HeartRateMonitor

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))

send_sos = False

start_time = time.time()

while True:
    heart_rate = round(hrm.get_heart_rate(), 2)
    
    if ((heart_rate > 120) or (heart_rate < 40)):
        if (abs(start_time - time.time()) > 30):
            send_sos = True
    else:
        start_time = time.time()
        send_sos = False
    
    '''
    # checking outputs
    print(f"Heart Rate: {heart_rate}")
    print(abs(start_time - time.time()))
    print(f"sos: {send_sos}\n")
    '''