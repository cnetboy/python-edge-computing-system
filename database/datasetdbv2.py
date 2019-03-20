from common.logger import get_logger
from common.userparameters import UserParameters
from config.configadapters import NODE, EDGE, CLOUD

my_logger = get_logger(__name__)

DATASET_CIFAR = "cifar"
DATASET_VOC = "voc"
DATASET_EPFL = "epfl"
DATASET_EPFL2 = "epfl2"
DATASET_IMAGENET = "imagenet"

from database.gcpdatasetdb import GcpDatasetDBV2
from database.pymongodatasetdb import PyMongoDatasetDBV2


class DatasetDBV2(object):

    def __init__(self, dataset_type):
        my_logger.info("Starting up Dataset Database.")
        self.dataset_db = factory_get_dataset_db(dataset_type)
        my_logger.info("Dataset Database has been initiated.")

    def insert_image_data(self, image_data):  # image must be RGB
        my_logger.info("Attempting to insert image.")
        self.dataset_db.insert_image_data(image_data)
        my_logger.info("Image has been inserted")

    def insert_annotation_data(self, annotation_data):
        my_logger.info("Attempting to insert label.")
        self.dataset_db.insert_annotation_data(annotation_data)
        my_logger.info("Label has been inserted")

    def insert_label_names(self, label_data):
        my_logger.info("Attempting to insert")
        self.dataset_db.insert_labels_data(label_data)
        my_logger.info("Label names has been inserted")

    def find_annotation_data(self, find_build):
        return self.dataset_db.find_annotation_data(find_build)

    def find_image_data(self, find_build):
        return self.dataset_db.find_image_data(find_build)

    def find_label_data(self, find_build):
        return self.dataset_db.find_label_data(find_build)


def factory_get_dataset_db(dataset_type):
    component = UserParameters().component
    system = UserParameters().get_system()
    if component == NODE:
        if system == 'WINDOWS':
            return PyMongoDatasetDBV2(dataset_type)
        else:
            return GcpDatasetDBV2()
    elif component == EDGE:
        return PyMongoDatasetDBV2(dataset_type)
    elif component == CLOUD:
        return GcpDatasetDBV2()
    else:
        raise Exception('Dataset DB not defined for component: ' + str(component))
