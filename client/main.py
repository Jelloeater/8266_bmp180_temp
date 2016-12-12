from time import sleep

__author__ = 'Jesse'
import data_client, env_sensor, json, esp, machine

SLEEP_TIMEOUT = 10

def data_send():
        json_to_send = json.dumps(env_sensor.Info().__dict__)
        data_client.send(json_to_send)

def run():
    while True:
        data_send()
        esp.deepsleep(1000000 * SLEEP_TIMEOUT)  #Goto deep sleep to save battery

if __name__ == "__main__":
    sleep(4)  # Wait for network
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')
        run()
    else:
        print('power on or hard reset')
        sleep(15)
        run()
