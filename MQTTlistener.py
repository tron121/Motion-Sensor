from discord.ext import tasks, commands
import paho.mqtt.client as mqtt
import config
import asyncio

class MQTTListenerCog(commands.Cog):

    def __init__(self):
        self.index = 0
        self.mqtt_capture.start()
        self.previous_status = None
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # self.mqtt_client.on_reconnect = self.on_reconnect
        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
        print("I have started the MQTT Cog.")

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() - if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("ECE2305Door/status")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        self.previous_status = config.door_status

        if msg.payload == "Door is opened!":
            #print("Received message opened")
            config.door_status = 'Opened'
            # Do something
        if msg.payload == "Door is closed!":
           #print("Received message closed")
            config.door_status = 'Closed'

    def cog_unload(self):
        self.mqtt_capture.cancel()

    @tasks.loop(seconds=.33)
    async def mqtt_capture(self):
        if config.is_ready is False:
            await asyncio.sleep(5)
        self.mqtt_client.loop_start()
        if config.door_status is None:
            self.mqtt_client.loop_start()
        else:
            print('Current Iteration: ' + str(self.index))
            print("Door Status is: " + str(config.door_status))

            config.seconds += .33
            if config.seconds>= 60:
                config.minutes+=1
                config.seconds=0
            if config.minutes==60:
                config.hours+=1
                config.minutes=0

            if self.previous_status is not None and self.previous_status != config.door_status:
                await config.general_channel.send("The door is now: " + config.door_status + ' ' + f"{config.alert_role.mention}")
                await config.general_channel.send('The door was: ' + str(self.previous_status) + ' for: '+ str(round(config.hours, 2)) +' Hours ' +
                                   str(round(config.minutes, 2)) + ' Minutes ' + str(round(config.seconds, 2)) + ' Seconds')
                config.seconds=0
                config.minutes=0
                config.hours=0
            self.index += 1
