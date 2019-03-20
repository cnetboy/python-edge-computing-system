import cv2
import pickle
import requests
import time
FILE_LOC = 'image.pkl'
test_file = 'D:\\Files\\Box Sync\\research\\source code\\Grit\\scripts\\data\\test_img1.png' #'test_people_1.jpg'
image_file = cv2.imread(test_file)
print('Size of request: ' + str(image_file.size))
pickle.dump(image_file, open(FILE_LOC, 'wb'))
data = {
        'cam': 1,
        'frame': 1,
    }
time_start = time.time()
resp = requests.post('http://192.168.1.70:8080/process/image/singleview', files={'file': open(FILE_LOC, 'rb')}, data=data, verify=False)
print('Processing Time: ' + str(time.time() - time_start))
print(str(resp.content))

#.47