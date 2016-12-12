from machine import I2C, Pin
from bmp180 import BMP180


class Info:
    def __init__(self):
        self.temp = None
        self.p = None
        self.altitude = None
        self.update()

    def update(self):
        # Returns object with temp, p, altitude
        bus = I2C(Pin(5), Pin(4), freq=9600)
        bmp180 = BMP180(bus)
        bmp180.oversample_sett = 2
        bmp180.baseline = 101325
        self.temp = bmp180.temperature
        self.p = bmp180.pressure
        self.altitude = bmp180.altitude
