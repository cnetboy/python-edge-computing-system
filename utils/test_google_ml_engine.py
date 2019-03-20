import cv2
import numpy as np
import sys
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
from googleapiclient.errors import HttpError

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

PROJECT_ID = "node-model-208923"
MODEL_NAME = "yolov2fullobjectdetector"
CREDENTIALS_FILE = "../config/node-model-ab1cf81d38ef.json"

# Connect to the Google Cloud ML service
credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
service = googleapiclient.discovery.build('ml', 'v1', credentials=credentials)

with open('test_img1.png', 'rb') as f:
    b64_x = f.read()
import base64
import json


image = cv2.imread('test_img1.png')
image_h, image_w, _ = image.shape
image = cv2.resize(image, (416, 416))
image = image / 255.

input_image = image[:,:,::-1]
input_image = np.expand_dims(input_image, 0)

input_instance = dict(input=input_image.tolist())
input_instance = json.loads(json.dumps(input_instance))

name = 'projects/' + PROJECT_ID + '/models/' + MODEL_NAME
request_body = {"instances": [input_instance]}

print(str(get_size(request_body)))
request = service.projects().predict(name=name, body=request_body)

try:
    response = request.execute()
    print(response)
except HttpError as err:
    print(err._get_reason())