## Network Integrated Motion Sensor 
This project was completed with a team as part of an Intro to Communications and Networks course. The project involves a magnetic door sensor connected to a Raspberry Pi to detect a person entering the room, and then reporting this information over the internet to a group of users via a Discord Bot Application. The RaspberryPi also captures camera images locally for later viewing. 

## Getting Started

### Prerequisites
* Raspberry Pi 3 or higher
* Raspberry Pi Camera Module
* Secondary device for running Discord Bot application
* Magnetic Reed sensor
### Installing on Raspberry Pi - Door Sensor Device
The Rasbperry Pi must have [Python 3.5 or later installed](https://www.python.org/downloads/), along with the following Python libraries:
* [RPi.GPIO Python Library](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
* [Eclipse Paho MQTT Python Library v1.5.0 or later](https://pypi.org/project/paho-mqtt/)
* [Picamera v1.13 or later](https://picamera.readthedocs.io/en/release-1.13/)
* [Pillow v7.1.1 or later](https://github.com/python-pillow/Pillow)

Some of these libraries are installed by default if the Raspberry Pi is imaged using the complete version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/), a variant of the Debian Operating System for specific use on the Raspberry Pi.

The reed sensor must be installed to the RaspberryPi using the GPIO pin, with one side of the sensor wire attached to the ground GPIO pin and one attached to a GPIO input pin (this implementation uses Pin 17). Once installed, the RaspberryPi must be connected to the internet, and the "Publisher.py" and "Subscriber.py" files must be run. The sensor can then be attached to a door to keep track of its status. This will be run constantly to publish the door status message via the MQTT protocol to the device running the Discord bot. 

Additionally, the Raspberry Pi Camera Module must be attached to its dedicated slot on the Pi itself. 

### Installing on Secondary Device - Discord Bot Device
The secondary device may be a personal computer, laptop, or another Raspberry Pi. It must have [Python 3.5 or later installed](https://www.python.org/downloads/), as well as the following Python Libraries:
* [discord.py v1.3.3 or later](https://discordpy.readthedocs.io/en/latest/index.html)
* [Picamera v1.13 or later](https://picamera.readthedocs.io/en/release-1.13/)
* [Pillow v7.1.1 or later](https://github.com/python-pillow/Pillow)
* [Eclipse Paho MQTT Python Library v1.5.0 or later](https://pypi.org/project/paho-mqtt/)

Once this secondary device is connected to the internet, the "GompeiBot.py" file must be run. This will allow for the GompeiBot Discord bot to be run which will alert those on the Discord server of the door sensor's status. 

## Additional Notes

### Setting up a Discord Application
This repository does not include the bot's private token, as it is intended to be self-hosted. If you wish to host your own version of the bot, you must create your own [Discord Developer Application](https://discordapp.com/developers/applications/), setup a Bot under that application, and use that Bot's generated token to replace the "my_token_here" line in the "GompeiBot.py" file. Accessing the Discord Developer page requires the creation of a free Discord account. 

## Built With
* [RPi.GPIO Python Library](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
  A method for controlling the Generic-Purpose Input/Output (GPIO) pins on the Raspberry Pi in order to retrive sensor input
* [Eclipse Paho MQTT Python Library](https://pypi.org/project/paho-mqtt/)
  Python implementation of the MQTT transfer protocol, allowing a bi-directional publisher/subscriber network between the Raspberry Pi and other devices.
* [Discord Developer API](https://discordapp.com/developers/docs)
  The Discord API which allows for custom programs to interface with Discord Chat Application
* [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
  A Python-based wrapper for the Discord API. Allows for development of Python programs to be used as Discord Applications
* [Picamera](https://picamera.readthedocs.io/en/release-1.13/) A Python library used to control the Raspberry Pi Camera Module
* [Pillow](https://github.com/python-pillow/Pillow) A Python library for image processing used on the Raspberry Pi. An actively-maintained fork of the now depreciated Python Imaging Library. 
