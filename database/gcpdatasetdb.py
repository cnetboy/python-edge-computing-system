from common.logger import get_logger

my_logger = get_logger(__name__)


class FakeLabelData(object):

    def __init__(self, label):
        self.label = label

    def get_name(self):
        return self.label


class GcpDatasetDBV2(object):

    def __init__(self):
        pass

    def insert_image_data(self, image_data):  # image must be RGB
        pass

    def insert_annotation_data(self, annotation_data):
        pass

    def insert_label_names(self, label_data):
        pass

    def find_annotation_data(self, find_build):
        pass

    def find_image_data(self, find_build):
        pass

    def find_label_data(self, find_build):
        labels = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor', 'unknown']
        return [FakeLabelData(label) for label in labels]

