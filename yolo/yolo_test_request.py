"""Perform test request"""
import pprint
import json
import requests

DETECTION_URL = "http://localhost:5000/v1/object-detection/yolov5s"
TEST_IMAGE = "yolo/cat.jpg"
image_url = "https://cdn.britannica.com/22/206222-131-E921E1FB/Domestic-feline-tabby-cat.jpg"

image_data = open(TEST_IMAGE, "rb").read()

# response = requests.post(DETECTION_URL, files={"image": image_data}).json()
# response = requests.post(DETECTION_URL, files={"image": image_data}, json={"image_url": image_url})
response = requests.post(DETECTION_URL, json={"image_url": image_url})

if response.ok:
    print("ok")

pprint.pprint(response)
# message.attachments.first().url
