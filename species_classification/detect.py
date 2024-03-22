'''
Loads in the model and starts capturing images from the Raspberry Pi camera module. 
The captured images are passed to the model and a confidence score is generated 
as to whether a shark was detected in the image or not. If a shark was detected,
the Pi communicates with the other Pi via serial communication to display a warning
'''

import tensorflow as tf
import os
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import cv2
import time
import sys
from image_capture import setup, take_picture, picam2
from load_model import model, analyze_image
import serial

BAUD_RATE = 9600

ser = serial.Serial('/dev/ttyS0', BAUD_RATE, timeout=1)

threshold = 0.9 # threshold to determine whether image contains a shark or not -- adjust this based on sensitivity
CAPTURED_IMAGES = './captured_images/' # Captured images from the Raspberry Pi camera

def send_msg(msg):
    """
    Sends a message via the serial port.

    Args:
        msg (str): The message to send.

    Returns:
        None
    """
    ser.write(msg.encode())

def capture_and_predict():
    """
    Uses the Raspberry Pi cmaera module to capture an image then 
    checks whether the image contains a shark or not based on whether 
    the confidence score is greater than the threshold

    Args:
        None

    Returns:
        None
    """
    while True:
        image_name = take_picture()
        img = cv2.imread(CAPTURED_IMAGES + image_name)
        confidence = analyze_image(img)
        if confidence > threshold:
            print(f"{image_name} is a shark")
            send_msg("shark")
        else:
            print(f"{image_name} is not a shark")
            send_msg("")
        print("-----------------------------------------")
        time.sleep(3)

setup()
capture_and_predict()