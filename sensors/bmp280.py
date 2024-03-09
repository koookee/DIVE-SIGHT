import smbus
import time

class BMP280:
    def __init__(self, bus=1, address=0x76):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.dig_T1 = self.read_unsigned_short(0x88)
        self.dig_T2 = self.read_signed_short(0x8A)
        self.dig_T3 = self.read_signed_short(0x8C)
        self.dig_P1 = self.read_unsigned_short(0x8E)
        self.dig_P2 = self.read_signed_short(0x90)
        self.dig_P3 = self.read_signed_short(0x92)
        self.dig_P4 = self.read_signed_short(0x94)
        self.dig_P5 = self.read_signed_short(0x96)
        self.dig_P6 = self.read_signed_short(0x98)
        self.dig_P7 = self.read_signed_short(0x9A)
        self.dig_P8 = self.read_signed_short(0x9C)
        self.dig_P9 = self.read_signed_short(0x9E)
        self.t_fine = 0

    def read_unsigned_byte(self, register):
        return self.bus.read_byte_data(self.address, register)

    def read_signed_byte(self, register):
        value = self.read_unsigned_byte(register)
        return value if value < 128 else value - 256

    def read_unsigned_short(self, register):
        low = self.read_unsigned_byte(register)
        high = self.read_unsigned_byte(register + 1)
        return (high << 8) + low

    def read_signed_short(self, register):
        value = self.read_unsigned_short(register)
        return value if value < 32768 else value - 65536

    def write_byte(self, register, value):
        self.bus.write_byte_data(self.address, register, value)

    def get_temperature(self):
        raw_temp = self.read_unsigned_short(0xFA)
        var1 = (raw_temp / 16384.0 - self.dig_T1 / 1024.0) * self.dig_T2
        var2 = ((raw_temp / 131072.0 - self.dig_T1 / 8192.0) * (raw_temp / 131072.0 - self.dig_T1 / 8192.0)) * self.dig_T3
        self.t_fine = int(var1 + var2)
        return (var1 + var2) / 5120.0

    def get_pressure(self):
        raw_pressure = self.read_unsigned_short(0xF7)
        var1 = (self.t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = (var2 / 4.0) + (self.dig_P4 * 65536.0)
        var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        p = 1048576.0 - raw_pressure
        p = (p - var2 / 4096.0) * 6250.0 / var1
        var1 = self.dig_P9 * p * p / 2147483648.0
        var2 = p * self.dig_P8 / 32768.0
        p = p + (var1 + var2 + self.dig_P7) / 16.0
        return p / 100.0  # Convert pressure to hPa