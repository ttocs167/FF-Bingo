from datetime import datetime
import picamera
from time import sleep
import asyncio

print("Initialising PiCam...")
camera = picamera.PiCamera(sensor_mode=6)
camera.resolution = (1280, 720)
camera.framerate_range = (0.16666, 20)
camera.start_preview()
camera.annotate_background = picamera.Color('black')

# Camera warm-up time
sleep(2)
# await asyncio.sleep(2)

print("PiCam ready!")


async def take_image():

    timestamp = datetime.now().strftime("%m_%d_%Y, %H-%M-%S")
    filename = "resources/plant_images/" + timestamp + ".jpg"
    camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.capture(filename, use_video_port=True)

    return filename
