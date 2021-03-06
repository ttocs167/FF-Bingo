import asyncio

import cv2
from datetime import datetime
import subprocess

cam_props = {'brightness': -10, 'contrast': 32, 'saturation': 128,
             'gain': 0, 'gamma': 150, 'sharpness': 4, 'exposure_auto': 3,
             'exposure_absolute': 10, 'exposure_auto_priority': 1,
             'white_balance_temperature_auto': 1}


def set_camera_settings():
    for key in cam_props:
        subprocess.call(['v4l2-ctl -d /dev/video0 -c {}={}'.format(key, str(cam_props[key]))],
                        shell=True)


async def take_image():

    print("initialising webcam...")
    set_camera_settings()

    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_EXPOSURE, 1)

    await asyncio.sleep(1)

    timestamp = datetime.now().strftime("%m_%d_%Y, %H-%M-%S")
    filename = "resources/plant_images/" + timestamp + ".png"
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame from camera!")
    else:
        cv2.imwrite(filename, frame)
        print("new image saved!")

    cam.release()
    return filename
