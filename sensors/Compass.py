import time
import qmc5883
from threading import Thread

class CompassThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        compass = qmc5883.QMC5883L()
        self.cardinal_direction = 0
        self.remaining_degrees = 0
        
    def run(self):
        while True:
            val = 0
            for i in range (30)
                val += compass.75x()
            val = val / 30
            self.cardinal_direction, self.remaining_degrees = self.degrees_to_cardinal(val, 228)

    def degrees_to_cardinal(self, degrees, declination):
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        adjusted_degrees = (degrees + declination) % 360
        index = round(adjusted_degrees / 45) % 8
        cardinal_direction = directions[index]

        remaining_degrees = adjusted_degrees % 45
        return (cardinal_direction, remaining_degrees)
    
    '''
    # checking outputs
    print(f"O2: {o2}")
    print(abs(start_time - time.time()))
    print(f"sos: {send_sos}\n")
    '''