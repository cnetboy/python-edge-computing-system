import json

from common.data_collector import DataCollector, DATA_TYPE_DETECTION
from common.userparameters import UserParameters
from database.datasetdbv2 import DatasetDBV2, DATASET_VOC
from database.builder.datasetbuilder import LabelFindBuilder
from database.weightsdb import get_weight
from thirdparty.kerasyolo.frontend import YOLO
from thirdparty.kerasyolo.utils import draw_boxes


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


class YoloV2Tiny(object):
    _instance = None

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__new__(self, *args, **kwargs)
            labels = DatasetDBV2(DATASET_VOC).find_label_data(LabelFindBuilder().build())
            self.label_array = [label.get_name() for label in labels]
            self.config = None
            config_loc = UserParameters().get_base_path() + '/thirdparty/kerasyolo/config.json'
            with open(config_loc) as config_buffer:
                self.config = json.load(config_buffer)

            self.model = YOLO(backend='Tiny Yolo',
                              input_size=self.config['model']['input_size'],
                              labels=self.label_array,
                              max_box_per_image=self.config['model']['max_box_per_image'],
                              anchors=self.config['model']['anchors'])

            weights_loc = get_weight('yolov2tinyvoc_v5.h5').replace('utils', '').replace('devices', '')
            self.model.load_weights(weights_loc)
        return self._instance

    def train(self, train_imgs, valid_imgs):
        self.model.train(train_imgs=train_imgs,
                   valid_imgs=valid_imgs,
                   train_times=self.config['train']['train_times'],
                   valid_times=self.config['valid']['valid_times'],
                   nb_epochs=self.config['train']['nb_epochs'],
                   learning_rate=self.config['train']['learning_rate'],
                   batch_size=self.config['train']['batch_size'],
                   warmup_epochs=self.config['train']['warmup_epochs'],
                   object_scale=self.config['train']['object_scale'],
                   no_object_scale=self.config['train']['no_object_scale'],
                   coord_scale=self.config['train']['coord_scale'],
                   class_scale=self.config['train']['class_scale'],
                   saved_weights_name=self.config['train']['saved_weights_name'],
                   debug=self.config['train']['debug'])
    
    def predict(self, image):
        boxes = self.model.predict(image)
        image_annotated = draw_boxes(image, boxes, self.label_array)
        boxes_str = 'Count: ' + str(len(boxes)) + ', ' + str([create_box_resp_field(box) for box in boxes])
        print('Results: ' + boxes_str)
        DataCollector().write(DATA_TYPE_DETECTION, boxes_str)
        return image_annotated, boxes