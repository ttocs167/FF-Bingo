from datetime import datetime
import PiCamera
from time import sleep

print("initialising Pi Camera...")
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Camera warm-up time
sleep(2)
# await asyncio.sleep(2)


async def take_image():

    timestamp = datetime.now().strftime("%m_%d_%Y, %H-%M-%S")
    filename = "resources/plant_images/" + timestamp + ".png"

    camera.capture(filename)

    return filename
