from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
from ssd1306 import SSD1306_128_32 as SSD1306
from mpu6050 import mpu6050
from max30102 import HeartRateMonitor
import qmc5883
import argparse
from gpiozero import Button, LED

class Display:

    def __init__(self):
        self.display = SSD1306(1)
        self.clear()
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.rotate = False

    def clear(self):
        self.display.begin()
        self.display.clear()
        self.display.display()

    def show(self):
        self.display.image(self.image)
        self.display.display()

def switch_lights():
    flashlight.toggle()
    sleep(0.5)
    
def degrees_to_cardinal(degrees, declination):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    adjusted_degrees = (degrees + declination) % 360
    index = round(adjusted_degrees / 45) % 8
    cardinal_direction = directions[index]

    remaining_degrees = adjusted_degrees % 45
    oled.draw.text((96, 0), f"{cardinal_direction}", fill=255)
    oled.draw.text((64, 11), f"{remaining_degrees:.2f} deg", fill=255)
    oled.show()
 
oled = Display()
compass = qmc5883.QMC5883L()
accelerometer = mpu6050(0x68)
flashlight_button = Button(17)
flashlight = LED(27)

oled.draw.text((0, 0), "Welcome to DIVE-SIGHT", fill=255)
oled.show()
sleep(3)
oled.draw.rectangle( [(0,0), (128, 32)], fill=0)

oled.draw.text((0, 0), "sensors starting...", fill=255)
oled.show()
sleep(3)
oled.draw.rectangle( [(0,0), (128, 32)], fill=0)

flashlight_button.when_pressed = switch_lights

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()


hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))

while True:
    # the sensor alteration code
    count = 0
    val = 0
    while (count < 30):
        val += compass.get_bearing()
        count += 1

    val = val / 30
    degrees_to_cardinal(val, 228)
    
    count = 0
    val_x = 0
    val_y = 0
    val_z = 0
    
    while (count < 10):
        m = accelerometer.get_accel_data()
        val_x += m['x']
        val_y += m['y']
        val_z += m['z']
        count += 1
    
    val_x = round(val_x / 10, 2)
    val_y = round(val_y / 10, 2)
    val_z = round(val_z / 10, 2)
    
    oled.draw.text((0, 0), f"x: {val_x}", fill=255)
    oled.draw.text((0, 11), f"y: {val_y}", fill=255)
    oled.draw.text((0, 22), f"z: {val_z}", fill=255)
    oled.show()
    
    sleep(7)
    
    oled.draw.rectangle( [(0,0), (128, 32)], fill=0)
    
    heart_rate = round(hrm.get_heart_rate(), 2)
    o2 = round(hrm.get_oxygen(), 2)
    
    oled.draw.text((0, 0), f"HR: {heart_rate}", fill=255)
    oled.show()
    
    oled.draw.text((0, 22), f"O2: {o2}", fill=255)
    oled.show()
    
    sleep(7)
    
    oled.draw.rectangle([(0,0), (128, 32)], fill=0)
    
    
    