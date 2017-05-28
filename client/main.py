from time import sleep

__author__ = 'Jesse'
import json, esp, machine
from machine import I2C, Pin
from bmp180 import BMP180
import socket

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
    def build_payload(data_in):
        headers = """\
        POST /auth HTTP/1.1\r
        Content-Type: {content_type}\r
        Content-Length: {content_length}\r
        Host: {host}\r
        Connection: close\r
        \r\n"""

        body = 'userName=Ganesh&password=pass'
        header = headers.format(
            content_type="application/x-www-form-urlencoded",
            content_length=len(body),
            host=str(HOST) + ":" + str(PORT)
        )
        payload = ''.join(header + body)
        print ("Payload: " + payload)
        return ''.join(payload).encode("utf-8")

    @staticmethod
    def send(data):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data_client.build_payload(data))
        finally:
            sock.close()
        print("Sent:     {}".format(data))

class env_sensor_Info:
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


if __name__ == "__main__":
    main.run()
