import random

from database.datasetdbv2 import DatasetDBV2
from database.builder.datasetbuilder import ImageFindBuilder


def split_data(dataset, train_percent):
    datasetDb = DatasetDBV2(dataset)
    findBuilder = ImageFindBuilder()
    findBuilder.build_result_columns("image_id")
    image_ids = datasetDb.find_image_data(findBuilder.build())
    image_ids = random.shuffle(image_ids)
    train_end_index = int(train_percent * len(image_ids))
    train_image_ids = image_ids[0:train_end_index]
    validate_image_ids = image_ids[train_end_index:]

    return train_image_ids, validate_image_ids
