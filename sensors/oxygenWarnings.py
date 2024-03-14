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

display_warning = False
send_sos = False

start_time = time.time()

while True:
    o2 = round(hrm.get_oxygen(), 2)
    
    if ((o2 > 100) or (o2 < 93)):
        if (abs(start_time - time.time()) > 30):
            send_sos = True
            display_warning = False
        elif (abs(start_time - time.time()) > 15):
            display_warning = True
    else:
        start_time = time.time()
        send_sos = False
        display_warning = False
    
    
    # checking outputs
    print(f"O2: {o2}")
    print(abs(start_time - time.time()))
    print(f"warning: {display_warning}")
    print(f"sos: {send_sos}\n")
    