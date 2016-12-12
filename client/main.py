__author__ = 'Jesse'
import data_client, env_sensor, ujson


def run():
    sensor_data = str(env_sensor.get())
    json_to_send = ujson.dumps(sensor_data)
    data_client.send(json_to_send)
    print('JSON TO SEND:  '+ json_to_send)


if __name__ == "__main__":
    run()
