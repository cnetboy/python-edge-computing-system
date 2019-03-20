from pymongo import MongoClient

from database.datasetdbv2 import DATASET_EPFL, DATASET_EPFL2, DATASET_VOC, DATASET_CIFAR, DATASET_IMAGENET
from database.collections.voccollection import *
from database.collections.cifarcollection import *
from database.collections.epflcollection import *
from database.collections.epfl2collection import *
from database.collections.imagenetcollection import *
from common.logger import get_logger

my_logger = get_logger(__name__)

SERVER = "localhost"
DB = "dataset"


class PyMongoDatasetDBV2(object):

    def __init__(self, dataset_type):
        my_logger.info("Starting up Dataset Database.")
        client = MongoClient(SERVER, 27017)
        self.collections = dataset_collection_factory(dataset_type, client[DB])
        my_logger.info("Dataset Database has been initiated.")

    def insert_image_data(self, image_data):  # image must be RGB
        my_logger.info("Attempting to insert image.")
        self.collections.insert_image_data(image_data)
        my_logger.info("Image has been inserted")

    def insert_annotation_data(self, annotation_data):
        my_logger.info("Attempting to insert label.")
        self.collections.insert_annotation_data(annotation_data)
        my_logger.info("Label has been inserted")

    def insert_label_names(self, label_data):
        my_logger.info("Attempting to insert")
        self.collections.insert_labels_data(label_data)
        my_logger.info("Label names has been inserted")

    def find_annotation_data(self, find_build):
        return self.collections.find_annotation_data(find_build)

    def find_image_data(self, find_build):
        return self.collections.find_image_data(find_build)

    def find_label_data(self, find_build):
        return self.collections.find_label_data(find_build)


def dataset_collection_factory(dataset_type, db):
    if dataset_type in DATASET_VOC:
        return VocCollections(
            db[VOC_COL_ANNOTATION],
            db[VOC_COL_IMAGES],
            db[VOC_COL_LABELS],
            )
    elif dataset_type in DATASET_CIFAR:
        return CifarCollections(
            db[CIFAR_COL_ANNOTATION],
            db[CIFAR_COL_IMAGES],
            db[CIFAR_COL_LABELS],
            )
    elif dataset_type in DATASET_EPFL:
        return EpflCollections(
            db[EPFL_COL_ANNOTATION],
            db[EPFL_COL_IMAGES],
            db[EPFL_COL_LABELS],
            )
    elif dataset_type in DATASET_EPFL2:
        return Epfl2Collections(
            db[EPFL2_COL_ANNOTATION],
            db[EPFL2_COL_IMAGES],
            db[EPFL2_COL_LABELS],
            )
    elif dataset_type in DATASET_IMAGENET:
        return ImagenetCollections(
            db[IMAGENET_COL_ANNOTATION],
            db[IMAGENET_COL_IMAGES],
            db[IMAGENET_COL_LABELS],
            )
    else:
        raise Exception("Dataset Collection not implemented: " + dataset_type)
