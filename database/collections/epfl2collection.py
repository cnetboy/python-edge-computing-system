from bson.binary import Binary, USER_DEFINED_SUBTYPE
import pickle

from common.logger import get_logger
from database.entities.epfl2datasetentities import Epfl2DatasetImage, Epfl2DatasetLabel, Epfl2DatasetAnnotation

my_logger = get_logger(__name__)

EPFL2_COL_ANNOTATION = 'epfl2_annotations'
EPFL2_COL_IMAGES = 'epfl2_images'
EPFL2_COL_LABELS = 'epfl2_labels'


class Epfl2Collections(object):
    def __init__(self, col_annotation, col_images, col_labels):
        self.col_annotation = col_annotation
        self.col_images = col_images
        self.col_labels = col_labels

    def insert_image_data(self, image_data):
        image_data = image_data.__dict__
        image_data['image'] = Binary(pickle.dumps(image_data['image']), subtype=USER_DEFINED_SUBTYPE)
        self.col_images.insert_one(image_data)

    def insert_annotation_data(self, annotation_data):
        label_data = annotation_data.get_dict()
        self.col_annotation.insert_one(label_data)

    def insert_labels_data(self, label_data):
        label_data = label_data.__dict__
        self.col_labels.insert_one(label_data)

    def find_annotation_data(self, find_build):
        results = self.col_annotation.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(Epfl2DatasetAnnotation(data['filename'], data['cam_num'], data['width'], data['height'], data['image_id'], data['source'], data['object']))
        return dataset
        my_logger.info("Annotation count found: " + str(len(dataset)))

    def find_image_data(self, find_build):
        results = self.col_images.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(Epfl2DatasetImage(data['cam_num'], data['image_id'], data['filename'], pickle.loads(data['image'])))
        return dataset
        my_logger.info("Images count found: " + str(len(dataset)))

    def find_label_data(self, find_build):
        results = self.col_labels.find(find_build)
        if results is None:
            return None
        dataset = list()
        for data in list(results):
            dataset.append(Epfl2DatasetLabel(data['source'], data['index'], data['name']))
        return dataset
        my_logger.info("Label count found: " + str(len(dataset)))
