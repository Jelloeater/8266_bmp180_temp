from time import sleep

__author__ = 'Jesse'
import data_client, env_sensor, json, esp, machine

SLEEP_TIMEOUT = 10

def data_send():
        json_to_send = json.dumps(env_sensor.Info().__dict__)
        data_client.send(json_to_send)

def run():
    sleep(4)  # Wait for network
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')
    else:
        print('power on or hard reset')
        sleep(5)
    while True:
        data_send()
        esp.deepsleep(500000 * SLEEP_TIMEOUT)  #Goto deep sleep to save battery

if __name__ == "__main__":
    run()
