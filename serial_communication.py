'''
Provides functions that allow two Raspberry Pi devices to communicate through the serial port
'''

import serial
import time
import sys

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyS0', BAUD_RATE)
    
def receive_msg():
    """
    Reads a message from the serial port and prints it to the console.
    """
    msg = ser.readline()
    print(msg)
    
def send_msg(msg):
    """
    Sends a message via the serial port.

    Args:
        msg (str): The message to send.

    Returns:
        None
    """
    ser.write(msg.encode())