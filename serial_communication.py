import serial
import time
import sys

ser = serial.Serial('/dev/ttyS0',9600)

if len(sys.argv) < 2:
    print("Must specifiy in argument to script whether to send or receive data")

if len(sys.argv) > 1 and sys.argv[1] == "send":
    msg = "Hello\n"
    ser.write(msg.encode())
elif len(sys.argv) > 1 and sys.argv[1] == "receive":
    msg = ser.readline()
    print(msg)
    