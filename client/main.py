from time import sleep

__author__ = 'Jesse'
import json, esp, machine
from machine import I2C, Pin
from bmp180 import BMP180
import urequests

SLEEP_TIMEOUT = 10
HOST, PORT = "192.168.1.16", 8080


class main:
    @staticmethod
    def run():
        sleep(4)  # Wait for network
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            print('woke from a deep sleep')
        else:
            print('power on or hard reset')
            sleep(5)
        while True:
            main.data_send()
            esp.deepsleep(500000 * SLEEP_TIMEOUT)  #Goto deep sleep to save battery

    @staticmethod
    def data_send():
            json_to_send = json.dumps(env_sensor_Info().__dict__)
            data_client.send(json_to_send)

class data_client:
    @staticmethod
    def send(data):
        r = urequests.post("http://192.168.1.16:8080/")
        print(r)
        print(r.content)
        print(r.text)
        print(r.content)
        print(r.json())

        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close()

class env_sensor_Info:
    def __init__(self):
        self.temp = None
        self.p = None
        self.altitude = None
        self.update()

    def update(self):
        # Returns object with temp, p, altitude
        bus = I2C(-1, Pin(5), Pin(4), freq=9600)
        bmp180 = BMP180(bus)
        bmp180.oversample_sett = 2
        bmp180.baseline = 101325
        self.temp = bmp180.temperature
        self.p = bmp180.pressure
        self.altitude = bmp180.altitude


if __name__ == "__main__":
    main.run()
