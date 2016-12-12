__author__ = 'Jesse'
import data_client, env_sensor, json


def run():
    json_to_send = json.dumps(env_sensor.get().__dict__)
    data_client.send(json_to_send)
    print('JSON TO SEND:  '+ json_to_send)


if __name__ == "__main__":
    run()
