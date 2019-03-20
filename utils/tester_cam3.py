import cv2
import pickle
import requests
import json

FILE_LOC = 'image.pkl'
test_file = 'D:\\Files\\Box Sync\\research\\source code\\BBox-Label-Tool\\Images\\001\\scene00026_cam2.jpg' #'test_people_1.jpg'
image_file = cv2.imread(test_file)
pickle.dump(image_file, open(FILE_LOC, 'wb'))
resp = requests.post('http://localhost:8080/process/image/quick', files={'file': open(FILE_LOC, 'rb')}, verify=False)
count = 1
while True:
    count = count + 1
    data = {
            'cam': 3,
            'frame': count,
            'prediction': resp.json()['prediction']
        }

    url = 'http://192.168.1.70:8080/process/image/multiview'
    resp = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data), verify=False)
    print(str(resp.content))