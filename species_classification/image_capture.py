from picamera2 import Picamera2, Preview
import time
import sys

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.options["quality"] = 95 # Sets the image quality to the highest value

# Show a preview of the camera feed if enable_preview is passed as an argument
# to the script
if 'enable_preview' in sys.argv: 
    picam2.start_preview(Preview.QTGL)

picam2.start()
time.sleep(3)

for i in range(0, 10):
    picam2.capture_file(f"images/image{i}.jpg")
    print(f"Captured image {i}")
    time.sleep(1)