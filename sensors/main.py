from max30102 import MAX30102
import threading
import time
from time import sleep
import numpy as np
from datetime import datetime
import numpy as np
import argparse
import qmc5883
from mpu6050 import mpu6050
from max30102 import MAX30102

# 25 samples per second
SAMPLE_FREQ = 25
# taking moving average of 4 samples when calculating HR
# in algorithm.h, "DONOT CHANGE" comment is attached
MA_SIZE = 4
# sampling frequency * 4 (in algorithm.h)
BUFFER_SIZE = 100

def calc_hr_and_spo2(ir_data, red_data):
    """
    By detecting  peaks of PPG cycle and corresponding AC/DC
    of red/infra-red signal, the an_ratio for the SPO2 is computed.
    """
    # get dc mean
    ir_mean = int(np.mean(ir_data))

    # remove DC mean and inver signal
    # this lets peak detecter detect valley
    x = -1 * (np.array(ir_data) - ir_mean)

    # 4 point moving average
    # x is np.array with int values, so automatically casted to int
    for i in range(x.shape[0] - MA_SIZE):
        x[i] = np.sum(x[i:i+MA_SIZE]) / MA_SIZE

    # calculate threshold
    n_th = int(np.mean(x))
    n_th = 30 if n_th < 30 else n_th  # min allowed
    n_th = 60 if n_th > 60 else n_th  # max allowed

    ir_valley_locs, n_peaks = find_peaks(x, BUFFER_SIZE, n_th, 4, 15)
    # print(ir_valley_locs[:n_peaks], ",", end="")
    peak_interval_sum = 0
    if n_peaks >= 2:
        for i in range(1, n_peaks):
            peak_interval_sum += (ir_valley_locs[i] - ir_valley_locs[i-1])
        peak_interval_sum = int(peak_interval_sum / (n_peaks - 1))
        hr = int(SAMPLE_FREQ * 60 / peak_interval_sum)
        hr_valid = True
    else:
        hr = -999  # unable to calculate because # of peaks are too small
        hr_valid = False

    # ---------spo2---------

    # find precise min near ir_valley_locs
    exact_ir_valley_locs_count = n_peaks

    # find ir-red DC and ir-red AC for SPO2 calibration ratio
    # find AC/DC maximum of raw

    # FIXME: needed??
    for i in range(exact_ir_valley_locs_count):
        if ir_valley_locs[i] > BUFFER_SIZE:
            spo2 = -999  # do not use SPO2 since valley loc is out of range
            spo2_valid = False
            return hr, hr_valid, spo2, spo2_valid

    i_ratio_count = 0
    ratio = []

    # find max between two valley locations
    # and use ratio between AC component of Ir and Red DC component of Ir and Red for SpO2
    red_dc_max_index = -1
    ir_dc_max_index = -1
    for k in range(exact_ir_valley_locs_count-1):
        red_dc_max = -16777216
        ir_dc_max = -16777216
        if ir_valley_locs[k+1] - ir_valley_locs[k] > 3:
            for i in range(ir_valley_locs[k], ir_valley_locs[k+1]):
                if ir_data[i] > ir_dc_max:
                    ir_dc_max = ir_data[i]
                    ir_dc_max_index = i
                if red_data[i] > red_dc_max:
                    red_dc_max = red_data[i]
                    red_dc_max_index = i

            red_ac = int((red_data[ir_valley_locs[k+1]] - red_data[ir_valley_locs[k]]) * (red_dc_max_index - ir_valley_locs[k]))
            red_ac = red_data[ir_valley_locs[k]] + int(red_ac / (ir_valley_locs[k+1] - ir_valley_locs[k]))
            red_ac = red_data[red_dc_max_index] - red_ac  # subtract linear DC components from raw

            ir_ac = int((ir_data[ir_valley_locs[k+1]] - ir_data[ir_valley_locs[k]]) * (ir_dc_max_index - ir_valley_locs[k]))
            ir_ac = ir_data[ir_valley_locs[k]] + int(ir_ac / (ir_valley_locs[k+1] - ir_valley_locs[k]))
            ir_ac = ir_data[ir_dc_max_index] - ir_ac  # subtract linear DC components from raw

            nume = red_ac * ir_dc_max
            denom = ir_ac * red_dc_max
            if (denom > 0 and i_ratio_count < 5) and nume != 0:
                # original cpp implementation uses overflow intentionally.
                # but at 64-bit OS, Pyhthon 3.X uses 64-bit int and nume*100/denom does not trigger overflow
                # so using bit operation ( &0xffffffff ) is needed
                ratio.append(int(((nume * 100) & 0xffffffff) / denom))
                i_ratio_count += 1

    # choose median value since PPG signal may vary from beat to beat
    ratio = sorted(ratio)  # sort to ascending order
    mid_index = int(i_ratio_count / 2)

    ratio_ave = 0
    if mid_index > 1:
        ratio_ave = int((ratio[mid_index-1] + ratio[mid_index])/2)
    else:
        if len(ratio) != 0:
            ratio_ave = ratio[mid_index]

    # why 184?
    # print("ratio average: ", ratio_ave)
    if ratio_ave > 2 and ratio_ave < 184:
        # -45.060 * ratioAverage * ratioAverage / 10000 + 30.354 * ratioAverage / 100 + 94.845
        spo2 = -45.060 * (ratio_ave**2) / 10000.0 + 30.054 * ratio_ave / 100.0 + 94.845
        spo2_valid = True
    else:
        spo2 = -999
        spo2_valid = False

    return hr, hr_valid, spo2, spo2_valid

def find_peaks(x, size, min_height, min_dist, max_num):
    """
    Find at most MAX_NUM peaks above MIN_HEIGHT separated by at least MIN_DISTANCE
    """
    ir_valley_locs, n_peaks = find_peaks_above_min_height(x, size, min_height, max_num)
    ir_valley_locs, n_peaks = remove_close_peaks(n_peaks, ir_valley_locs, x, min_dist)

    n_peaks = min([n_peaks, max_num])

    return ir_valley_locs, n_peaks


def find_peaks_above_min_height(x, size, min_height, max_num):
    """
    Find all peaks above MIN_HEIGHT
    """

    i = 0
    n_peaks = 0
    ir_valley_locs = []  # [0 for i in range(max_num)]
    while i < size - 1:
        if x[i] > min_height and x[i] > x[i-1]:  # find the left edge of potential peaks
            n_width = 1
            # original condition i+n_width < size may cause IndexError
            # so I changed the condition to i+n_width < size - 1
            while i + n_width < size - 1 and x[i] == x[i+n_width]:  # find flat peaks
                n_width += 1
            if x[i] > x[i+n_width] and n_peaks < max_num:  # find the right edge of peaks
                # ir_valley_locs[n_peaks] = i
                ir_valley_locs.append(i)
                n_peaks += 1  # original uses post increment
                i += n_width + 1
            else:
                i += n_width
        else:
            i += 1

    return ir_valley_locs, n_peaks


def remove_close_peaks(n_peaks, ir_valley_locs, x, min_dist):
    """
    Remove peaks separated by less than MIN_DISTANCE
    """

    # should be equal to maxim_sort_indices_descend
    # order peaks from large to small
    # should ignore index:0
    sorted_indices = sorted(ir_valley_locs, key=lambda i: x[i])
    sorted_indices.reverse()

    # this "for" loop expression does not check finish condition
    # for i in range(-1, n_peaks):
    i = -1
    while i < n_peaks:
        old_n_peaks = n_peaks
        n_peaks = i + 1
        # this "for" loop expression does not check finish condition
        # for j in (i + 1, old_n_peaks):
        j = i + 1
        while j < old_n_peaks:
            n_dist = (sorted_indices[j] - sorted_indices[i]) if i != -1 else (sorted_indices[j] + 1)  # lag-zero peak of autocorr is at index -1
            if n_dist > min_dist or n_dist < -1 * min_dist:
                sorted_indices[n_peaks] = sorted_indices[j]
                n_peaks += 1  # original uses post increment
            j += 1
        i += 1

    sorted_indices[:n_peaks] = sorted(sorted_indices[:n_peaks])

    return sorted_indices, n_peaks


class HeartRateMonitor(object):
    """
    A class that encapsulates the max30102 device into a thread
    """

    LOOP_TIME = 1

    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print('IR, Red')
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []
        
        bpm_high = []
        bpm_low = []
        o2_high = []
        o2_low = []

        # Run until told to stop.
        while not self._thread.stopped:
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # Put all data into arrays.
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)
                    if self.print_raw:
                        print("{0}, {1}".format(ir, red), file=open('/home/rayah/Documents/health.txt', 'a'))

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                         
                    bpm, valid_bpm, spo2, valid_spo2 = calc_hr_and_spo2(ir_data, red_data)
                    if valid_bpm:
                        bpms.append(bpm)
                        while len(bpms) > 4:
                            bpms.pop(0)
                        self.bpm = np.mean(bpms)
                        if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                            self.bpm = 0
                            if self.print_result:
                                print("Person not detected at {0}".format(datetime.now().strftime("%H:%M:%S")), file=open('/home/rayah/Documents/health.txt', 'a'))
                        elif self.print_result:
                            
                            print("Low BPM: {0}, High BPM: {1}, Low O2: {2}, High O2: {3}\nBPM: {4}, SpO2: {5}, Time: {6}, ".format(bpm_low, bpm_high, o2_low,
                            o2_high, round(self.bpm, 2),round(spo2, 2), datetime.now().strftime("%H:%M:%S")),
                            file=open('/home/rayah/Documents/health.txt', 'a'))
                            
                            #Checking if the heart rate is too low
                            if(40 > self.bpm):
                                bpm_low.append(self.bpm)
                                if(len(bpm_low)>=120):
                                    print("SOS HEART RATE IS LOW", file=open('/home/rayah/Documents/health.txt', 'a'))
                                elif(len(bpm_low)>=10):
                                    print("WARNING: HEART RATE IS LOW", file=open('/home/rayah/Documents/health.txt', 'a'))
                            else:
                                bpm_low.clear()
                                
                            #Checking if the heart rate is too high
                            if(120 < self.bpm):
                                bpm_high.append(self.bpm)
                                if(len(bpm_high)>=120):
                                    print("SOS HEART RATE IS HIGH", file=open('/home/rayah/Documents/health.txt', 'a'))
                                elif(len(bpm_high)>=10):
                                    print("WARNING: HEART RATE IS HIGH", file=open('/home/rayah/Documents/health.txt', 'a'))
                            else:
                                bpm_high.clear()
                                #clear the array
                                
                            #Checking if the blood oxygen is too low hypotoxia)
                            if(93 > spo2):
                                o2_low.append(spo2)
                                if(len(o2_low)>=120):
                                    print("SOS BLOOD OXYGEN IS LOW", file=open('/home/rayah/Documents/health.txt', 'a'))
                                elif(len(o2_low)>=10):
                                    print("WARNING: BLOOD OXYGEN IS LOW", file=open('/home/rayah/Documents/health.txt', 'a'))
                            else:
                                o2_low.clear()
                                                                
                            #Checking if the blood oxygen is too high (hypertoxia)
                            if(100 < spo2):
                                o2_high.append(spo2)
                                if(len(o2_high)>=120):
                                    print("SOS BLOOD OXYGEN IS HIGH", file=open('/home/rayah/Documents/health.txt', 'a'))
                                elif(len(o2_high)>=10):
                                    print("WARNING: BLOOD OXYGEN IS HIGH", file=open('/home/rayah/Documents/health.txt', 'a'))
                            else:
                                o2_high.clear()
                            
            time.sleep(self.LOOP_TIME)

        #sensor.shutdown()

    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()

    def stop_sensor(self, timeout=2.0):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join(timeout)

open("/home/rayah/Documents/health.txt", "w").close

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

compass = qmc5883.QMC5883L()
accelerometer = mpu6050(0x68)

print('sensors starting...', file=open('/home/rayah/Documents/health.txt', 'a'))
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()

while True:
    m = compass.get_bearing()
    if (0 < m < 90):
        print("north", file=open('/home/rayah/Documents/health.txt', 'a'))
        sleep(3)

    elif (90 < m < 180):
        print ("east", file=open('/home/rayah/Documents/health.txt', 'a'))
        sleep(3)

    elif (180 < m < 270):
        print("south", file=open('/home/rayah/Documents/health.txt', 'a'))
        sleep(3)

    elif (270 < m < 360):
        print("west", file=open('/home/rayah/Documents/health.txt', 'a'))
        sleep(3)
        
    accel_data = accelerometer.get_accel_data()

    print("x: " + str(accel_data['x']), file=open('/home/rayah/Documents/health.txt', 'a'))
    print("y: " + str(accel_data['y']), file=open('/home/rayah/Documents/health.txt', 'a'))
    print("z: " + str(accel_data['z']), file=open('/home/rayah/Documents/health.txt', 'a'))
    
try:
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...', file=open('/home/rayah/Documents/health.txt', 'a'))

#hrm.stop_sensor()
#print('sensor stopped!', file=open('/home/rayah/Documents/1/health.txt', 'a'))