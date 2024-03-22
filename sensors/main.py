import time
from threading import Thread
from Accelerometer import AccelerometerThread
from HeartRate import HeartRateThread
from OxygenLevels import OxygenThread
from MarineLife import MarineLifeThread
from ssd1306 import SSD1306_128_32 as SSD1306
from PIL import Image, ImageDraw, ImageFont, ImageOps


class Display():
    def __init__(self):
        self.display = SSD1306(1)
        self.clear()
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.rotate = False
        
    def run(self):
        ...

    def clear(self):
        self.display.begin()
        self.display.clear()
        self.display.display()

    def show(self):
        self.display.image(self.image)
        self.display.display()

oled = Display()
accelerometer = AccelerometerThread()
heart_rate = HeartRateThread()
oxygen_levels = OxygenThread()
marine_life = MarineLifeThread()

accelerometer.start()
heart_rate.start()
oxygen_levels.start()
marine_life.start()

while True:
    time.sleep(1)
    warnings = []
    if accelerometer.send_sos:
        warnings.append("falling unconscious")
    if heart_rate.send_sos:
        warnings.append("irregular heart rate")
    if oxygen_levels.send_sos:
        warnings.append("irregular oxygen levels")
    if marine_life.warning:
        warnings.append("shark detected")

    if len(warnings) > 0:
        warnings.insert(0, f"{len(warnings)} warning(s)")
        row = 0
        for idx in range(0,len(warnings),2):
            warning1 = warnings[idx]
            if idx+1 < len(warnings):
                warning2 = warnings[idx+1]
            else:
                warning2 = ""
            warnings_str = warning1 + " | " warning2
            oled.draw.text((0, row * 11), warnings_str, fill=255)
            row += 1
            print(warnings_str)
        
    else:
        print(f"Heart Rate: {heart_rate.heart_rate}")
        print(f"Oxygen Levels: {oxygen_levels.o2}")
        print(f"Accelerometer Readings: {accelerometer.val_x}, {accelerometer.val_y}, {accelerometer.val_z}")
        oled.draw.text((0, 0), f"Heart Rate: {heart_rate.heart_rate}", fill=255)
        oled.draw.text((0, 11), f"Oxygen Levels: {oxygen_levels.o2}", fill=255)
        oled.draw.text((0, 22), f"Acc: {accelerometer.val_x:.1f}, {accelerometer.val_y:.1f}, {accelerometer.val_z:.1f}", fill=255)
        oled.show()
        oled.draw.rectangle( [(0,0), (128, 32)], fill=0)