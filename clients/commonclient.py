import pickle
import requests
import time

from clients.generalresponse import GeneralResponse
from clients.responsestatus import ResponseStatus
from common.data_collector import DataCollector, DATA_TYPE_DATA_TRANSFER_TIME, DATA_TYPE_TRANSFER_SIZE, DATA_TYPE_DETECTION, DATA_TYPE_COMPUTING_TIME
from common.userparameters import UserParameters
from thirdparty.kerasyolo.utils import draw_boxes2

PICKLED_TEMP_LOC = UserParameters().get_base_path() + '\\clients\\temp\\preprocessimage.pkl'
SINGLE_VIEW_RELATIVE_URL = "/process/image/singleview"
MULTI_VIEW_RELATIVE_URL = "/process/image/multiview"
MODEL_WEIGHT_UPDATE_SERVICE_URL = ""

def get_status(endpoint_status):
    return ResponseStatus.SUCCESS

def get_image(image, predictions):
    if len(predictions) <= 0:
        return image
    else:
        if UserParameters().get_none_node_model() == 'YOLOV2':
            label_array = [
                'background',
                'aeroplane',
                'bicycle',
                'bird',
                'boat',
                'bottle',
                'bus',
                'car',
                'cat',
                'chair',
                'cow',
                'diningtable',
                'dog',
                'horse',
                'motorbike',
                'person',
                'pottedplant',
                'sheep',
                'sofa',
                'train',
                'tvmonitor',
                'unknown',
                'basketball' # may need to remove
            ]
        else:
            label_array = [
                'tvmonitor',
                'train',
                'person',
                'boat',
                'horse',
                'cow',
                'bottle',
                'dog',
                'aeroplane',
                'car',
                'bus',
                'bicycle',
                'chair',
                'diningtable',
                'pottedplant',
                'bird',
                'cat',
                'motorbike',
                'sheep',
                'sofa',
                'background',
            ]
        return draw_boxes2(image, predictions, label_array)


def send_request(url, request):
    print('Size of request: ' + str(request.image.size))

    start_time = time.time()

    # Send full image to edge device for further processing
    pickle.dump(request.image, open(PICKLED_TEMP_LOC, 'wb'))

    resp = requests.post(url, files={'file': open(PICKLED_TEMP_LOC, 'rb')}, verify=False)
    status_code = resp.status_code
    size_of_resp = len(resp.content)
    total_size = str(request.image.size + size_of_resp)
    resp = resp.json()

    print('Size of response: ' + str(size_of_resp))
    print('Total bandwidth usage: ' + total_size)

    duration = str(time.time() - start_time)
    prediction = 'Count: ' + str(len(resp['prediction'])) + ', ' + str(resp['prediction'])
    print('Data Transfer Time: ' + duration)
    print('Results: ' + prediction)

    data_collector = DataCollector()
    data_collector.write(DATA_TYPE_TRANSFER_SIZE, total_size)
    data_collector.write(DATA_TYPE_DATA_TRANSFER_TIME, duration)
    data_collector.write(DATA_TYPE_DETECTION, prediction)

    computational_times = resp['computational_time']
    for index, comp_time in enumerate(computational_times):
        data_collector.write(DATA_TYPE_COMPUTING_TIME + '_' + str(index + 1), comp_time)

    return GeneralResponse(get_status(status_code), get_image(request.image, resp['prediction']), resp['prediction'], resp['computational_time'])
