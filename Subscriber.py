import paho.mqtt.client as mqtt
import webbrowser
from io import BytesIO
import time
from picamera import PiCamera

camera_delay = 10
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ECE2305Door/status")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")

    #print(msg.topic+" "+str(msg.payload))

    if msg.payload == "Door is opened!":
        global camera_delay
        print("Received message opened")
        #print(door_status)
        if camera_delay == 0:
            camera = PiCamera()
            camera.resolution = (1024, 768)
            camera.start_preview()
            print("Taking an image...")
            time.sleep(2)
            data = time.strftime("%Y-%b-%d_(%H%M%S)")
            camera.capture('%s.jpg'%data)
            print("Photo Captured")
            camera.close()
            print("Camera Closed")
            camera_delay = 10
        else:
            camera_delay = camera_delay - 1
            sleep(1)
            print("Waiting...")

    if msg.payload == "Door is closed!":
        print("Received message closed")


# Create an MQTT client and attach our routines to it.

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
camera_delay = 0
client.connect("test.mosquitto.org", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
#TODO: Look into just using the loop() function
client.loop_forever()
