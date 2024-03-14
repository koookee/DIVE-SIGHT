import serial

ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    x = ser.readline()
    print(x)
    time.sleep(0.5)