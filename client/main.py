from time import sleep

__author__ = 'Jesse'
import json, esp, machine
from machine import I2C, Pin
from bmp180 import BMP180
import urequests as requests

INITIAL_SLEEP_TIMEOUT = 60 * 5 * 1000000  # Seconds x Minutes
SLEEP_TIMEOUT = 60 * 30 * 1000000  # Seconds
RETRY_SLEEP_TIMEOUT = 60 * 1 * 1000000  # Seconds x Minutes


class main:
    @staticmethod
    def run():
        sleep(5)  # Wait for network
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            # Deep Sleep Wake
            if main.data_send():
                esp.deepsleep(SLEEP_TIMEOUT)
            else:
                esp.deepsleep(RETRY_SLEEP_TIMEOUT)
        else:
            # Initial Boot
            print("Initial Boot")
            if main.data_send():
                esp.deepsleep(INITIAL_SLEEP_TIMEOUT)
            else:
                esp.deepsleep(RETRY_SLEEP_TIMEOUT)

    @staticmethod
    def data_send():
        """ Returns True if data was sent
        """
        json_to_send = json.dumps(env_sensor_Info().__dict__)
        try:
            url = "http://192.168.22.16:8080"
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json_to_send, headers=headers)
            print(r.__dict__)
            r.close()
            return True
        except OSError:
            print('Connection Failure')
            return False


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
