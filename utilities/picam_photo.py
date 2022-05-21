from datetime import datetime
from picamera import PiCamera
from time import sleep

print("Initialising PiCam...")
camera = PiCamera()
camera.resolution = (1640, 1232)
camera.framerate_range = (0.16666, 60)
camera.start_preview()
camera.annotate_background = PiCamera.Color('black')

# Camera warm-up time
sleep(2)
# await asyncio.sleep(2)

print("PiCam ready!")


async def take_image():

    timestamp = datetime.now().strftime("%m_%d_%Y, %H-%M-%S")
    filename = "resources/plant_images/" + timestamp + ".png"
    camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.capture(filename)

    return filename
