import cv2
from datetime import datetime


async def take_image():

    print("initialising webcam...")
    cam = cv2.VideoCapture(0)

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
