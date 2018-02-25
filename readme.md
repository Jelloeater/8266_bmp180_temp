# 8266 BMP Temp Grapher
**A Micro Python Project to display temprature readins in JSON for query**

* Runs on a ESP8266 NodeMCU or WeMOS D1 mini
* Thanks to https://github.com/micropython-IMU/micropython-bmp180 for the library!

## Server
Build commands (run from server directory)

    docker volume create 8266_data_vol
    docker build -t 8266_api_img .

Run in order, for each component (if none specified, just run the web server):

    docker run -d --name 8266_api -p 8080:8080 -v 8266_data_vol:/data 8266_api_img "./temp_server.py"

To run:

    docker start 8266_api

See Dockerfile for info

## Client
* **Uses I2C on Pin 5 and Pin4 at freq = 9600**
* You will need a **BMP180 temp sensor** wired to pins 4 and 5.
* Copy all files to 8266
* After that it should auto boot to the script
* You will also need to have deep sleep wired up properly.

* See https://github.com/adafruit/ampy for pushing files