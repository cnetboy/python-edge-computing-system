import clients.commonclient as cc
from clients.cloudclient import SINGLE_VIEW_RELATIVE_URL, MULTI_VIEW_RELATIVE_URL
import json
import pickle
from pympler import asizeof
import requests
import time

from clients.noderesponse import NodeResponse
from clients.responsestatus import ResponseStatus
from common.data_collector import DataCollector, DATA_TYPE_DATA_TRANSFER_TIME, DATA_TYPE_TRANSFER_SIZE, DATA_TYPE_DETECTION
from common.userparameters import UserParameters
from thirdparty.kerasyolo.utils import draw_boxes2


PICKLED_TEMP_LOC = "D:\\Files\\Box Sync\\research\\source code\\E_System\\clients\\temp\\preprocessimage.pkl"


def create_box_resp_field(box):
    resp_fields = dict()
    resp_fields['label'] = int(box.label)
    resp_fields['score'] = float(box.score)
    resp_fields['xmax'] = float(box.xmax)
    resp_fields['xmin'] = float(box.xmin)
    resp_fields['ymax'] = float(box.ymax)
    resp_fields['ymin'] = float(box.ymin)
    return\
        resp_fields


def post_to_single_view(request):
    return cc.send_request(str(UserParameters().get_edge_ip()) + SINGLE_VIEW_RELATIVE_URL, request)


def post_to_multi_view(request):
    data = {
        'cam': request.cam_num,
        'frame': request.frame_num,
        'prediction': [create_box_resp_field(pred) for pred in request.predicted_box_loc]
    }

    size_of_request = asizeof.asizeof(data)
    print('Size of request: ' + str(size_of_request))

    start_time = time.time()

    resp = requests.post(str(UserParameters().get_edge_ip()) + MULTI_VIEW_RELATIVE_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(data), verify=False)
    status_code = resp.status_code
    size_of_resp = asizeof.asizeof(resp.content)
    total_size = str(size_of_request + size_of_resp)
    resp = resp.json()
    print('Size of response: ' + str(size_of_resp))
    print('Total transfer size: ' + total_size)

    duration = str(time.time() - start_time)
    prediction = 'Count: ' + str(len(resp['prediction'])) + ', ' + str(resp['prediction'])
    print('Data Transfer Time: ' + duration)
    print('Results: ' + prediction)

    data_collector = DataCollector()
    data_collector.write(DATA_TYPE_TRANSFER_SIZE, total_size)
    data_collector.write(DATA_TYPE_DATA_TRANSFER_TIME, duration)
    data_collector.write(DATA_TYPE_DETECTION, prediction)

    return NodeResponse(cc.get_status(status_code), cc.get_image(request.image, resp['prediction']), resp['prediction'])


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
    print('Total transfer size: ' + total_size)

    duration = str(time.time() - start_time)
    prediction = 'Count: ' + str(len(resp['prediction'])) + ', ' + str(resp['prediction'])
    print('Data Transfer Time: ' + duration)
    print('Results: ' + prediction)

    data_collector = DataCollector()
    data_collector.write(DATA_TYPE_TRANSFER_SIZE, total_size)
    data_collector.write(DATA_TYPE_DATA_TRANSFER_TIME, duration)
    data_collector.write(DATA_TYPE_DETECTION, prediction)

    return NodeResponse(cc.get_status(status_code), cc.get_image(request.image, resp['prediction']), resp['prediction'])


def post_to_model_weight_update_service(request):
    return cc.send_request(MODEL_WEIGHT_UPDATE_SERVICE_URL, request)
