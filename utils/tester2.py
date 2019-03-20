import cv2
import pickle
import requests

FILE_LOC = 'image.pkl'
test_file = 'D:\\Files\\Box Sync\\research\\source code\\BBox-Label-Tool\\Images\\001\\scene00026_cam2.jpg' #'test_people_1.jpg'
image_file = cv2.imread(test_file)
print('Size of request: ' + str(image_file.size))
pickle.dump(image_file, open(FILE_LOC, 'wb'))
data = {
        'cam': 2,
        'frame': 1,
    }
resp = requests.post('http://localhost:8080/process/image/full', files={'file': open(FILE_LOC, 'rb')}, data=data, verify=False)
print(str(resp.content))
