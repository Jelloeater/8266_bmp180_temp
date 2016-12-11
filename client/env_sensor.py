def get():
    #Returns temp, p, altitude
    from machine import I2C, Pin
    from bmp180 import BMP180

    bus =  I2C(Pin(5), Pin(4),freq=9600)
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325
    temp = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude
    return {'temp':temp, 'p':p, 'altitude':altitude}
