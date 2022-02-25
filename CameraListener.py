from discord.ext import tasks, commands
import config
import asyncio
import io
import socket
import struct
from PIL import Image

class CameraListenerCog(commands.Cog):

    def __init__(self):
        self.index = 0
        self.camera_capture.start()
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)
        print("Socket Connected")

        # Accept a single connection and make a file-like object out of it
        self.connection = self.server_socket.accept()[0].makefile('rb')
        print("I have started the Camera Cog.")

    def cog_unload(self):
        self.connection.close()
        self.server_socket.close()
        self.camera_capture.cancel()

    @tasks.loop(seconds=1.0)
    async def camera_capture(self):
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            print("No image detected")
        if image_len:
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(self.connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            print('Image is %dx%d' % image.size)
            image.show()
            image.verify()
            print('Image is verified')
            # image.show()
        self.index += 1
        print(self.index)
