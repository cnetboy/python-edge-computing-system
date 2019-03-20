from model.multiviewmanager import MultiviewManager
from thirdparty.kerasyolo.utils import draw_boxes
from common.data_collector import DataCollector, DATA_TYPE_DETECTION
import time

WAIT_TIME_LIMT = 60


def create_box_resp_field(box):
    resp_fields = dict()
    resp_fields['label'] = int(box.label)
    resp_fields['score'] = float(box.score)
    resp_fields['xmax'] = float(box.xmax)
    resp_fields['xmin'] = float(box.xmin)
    resp_fields['ymax'] = float(box.ymax)
    resp_fields['ymin'] = float(box.ymin)
    return resp_fields


LABEL_ARRAY = [
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
        ]


class MultiviewDetector(object):

    def predict(self, frame_num, cam_num, image):
        manager = MultiviewManager()
        manager.manage_data(frame_num, cam_num, image)
        boxes = []
        init_time = time.time()
        while (time.time() - init_time) <= WAIT_TIME_LIMT:
            if manager.is_result_exist(frame_num):
                boxes = manager.get_results(frame_num, cam_num)
                break
        return None, boxes