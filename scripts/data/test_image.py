import cv2

from database.builder.datasetbuilder import ImageFindBuilder
from database.datasetdbv2 import DatasetDBV2, DATASET_IMAGENET


def display_image():
    datasetDb = DatasetDBV2(DATASET_IMAGENET)
    find_builder = ImageFindBuilder()
    find_builder.build_image_id('n02802426_10083')
    data = datasetDb.find_image_data(find_builder.build())
    for index, item in enumerate(data):
        cv2.imwrite('test_img' + str(index + 1) + '.png', item.get_image())
        image = cv2.imread('test_img.png')
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


display_image()
