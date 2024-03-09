import BMP280

bmp = bmp280.BMP280()
temperature = bmp.get_temperature()
pressure = bmp.get_pressure()
print(f"Temperature: {temperature:.2f} C, Pressure: {pressure:.2f} hPa")