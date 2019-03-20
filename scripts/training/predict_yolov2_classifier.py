from model.archive.yolotinyv2classifier import YoloTinyClassifier
from database.builder.datasetbuilder import ImageFindBuilder
from database.datasetdbv2 import DatasetDBV2, DATASET_CIFAR


def predict():
    databaseDb = DatasetDBV2(DATASET_CIFAR)
    image_find_builder = ImageFindBuilder()
    image_find_builder.build_image_id_gte_lte(6, 10)
    image_data = databaseDb.find_image_data(image_find_builder.build())
    classifier = YoloTinyClassifier()
    for data in image_data:
        results = classifier.predict(data.get_image())
        print(str(results) + '\n')

predict()