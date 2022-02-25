import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time
import sys
import signal

#GPIO Setup
GPIO.setmode(GPIO.BCM)
MAGNET_GPIO = 17
GPIO.setup(MAGNET_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if (GPIO.input(MAGNET_GPIO)) == 1:
        publish.single("ECE2305Door/status", "Door is opened!",
                       hostname="test.mosquitto.org")
        print ('Door is opened!')
    if (GPIO.input(MAGNET_GPIO)) == 0:
        publish.single("ECE2305Door/status", "Door is closed!",
                       hostname="test.mosquitto.org")
        print ('Door is closed!')
    time.sleep(0.1)
