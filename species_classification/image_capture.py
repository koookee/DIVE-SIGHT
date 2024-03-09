'''
Contains the functions for seting up the Raspberry Pi camera module and taking pictures
'''

from picamera2 import Picamera2, Preview
import time
import sys

picam2 = Picamera2()

def setup():
    '''
    Setup and configure the Raspberry Pi camera module
    '''
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.options["quality"] = 95 # Sets the image quality to the highest value
    picam2.start()
    time.sleep(3)

# Show a preview of the camera feed if enable_preview is passed as an argument
# to the script
if 'enable_preview' in sys.argv: 
    picam2.start_preview(Preview.QTGL)

def take_picture():
    '''
    Take a picture with the camera moule and save the image to a folder
    '''
    epoch_time = int(time.time())
    picam2.capture_file(f"captured_images/image{epoch_time}.jpg")
    print(f"Captured image {epoch_time}")
    return f"image{epoch_time}.jpg"