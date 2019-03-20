import cv2
import json
import glob
import re

from database.datasetdbv2 import DatasetDBV2, DATASET_EPFL2
from database.entities.epfl2datasetentities import Epfl2DatasetAnnotationObject, Epfl2DatasetAnnotation, Epfl2DatasetImage

ANNOTATION_BASE_LOCATION = 'D:\\Files\\BigFiles\\EPFL-RLC_dataset\\multiclass_ground_truth\\bounding_boxes_EPFL_cross\\'
IMAGE_BASE_LOCATION = 'D:\\Files\\BigFiles\\EPFL-RLC_dataset\\multiclass_ground_truth_images\\'


def get_image_id(file_name):
    image_id = re.search('(det_frame)(\d+)', file_name).group(2)
    return image_id


def get_cam_num(file_name):
    cam_num = re.search('(cam)(\d+)', file_name).group(2)
    return cam_num


def get_objs(label, file_name):
    objs = list()
    file_content = None
    with open(file_name, 'r') as f:
        file_content = f.read()

    if file_content is not None:
        file_content = file_content.split()
        for index, item in enumerate(file_content):
            if index*4 >= len(file_content):
                break
            xmin = file_content[index * 4]
            ymin = file_content[(index * 4) + 1]
            xmax = file_content[(index * 4) + 2]
            ymax = file_content[(index * 4) + 3]
            objs.append(Epfl2DatasetAnnotationObject(label, xmin, ymin, xmax, ymax))
    return objs


def get_annotations(labels_folder):
    annotations = dict()

    for folder_item in labels_folder:
        annotation_files = glob.glob(ANNOTATION_BASE_LOCATION + folder_item[1] + '\\visible_frame\\*.txt')
        for file in annotation_files:
            cam_num = get_cam_num(file)
            width = 360
            height = 288
            image_id = get_image_id(file)
            source = 'EPFL2'
            objs = get_objs(folder_item[0], file)
            ann = Epfl2DatasetAnnotation(file, cam_num, width, height, image_id, source, objs)

            if image_id + cam_num not in annotations:
                annotations[image_id + cam_num] = ann
            else:
                for obj in ann.get_objects():
                    annotations[image_id + cam_num].add_object(obj)

    return annotations


def get_images(num_images, annotation_cam_imageids):
    image_data = list()

    for num in range(num_images):
        image_files = glob.glob(IMAGE_BASE_LOCATION + 'c' + str(num) + '\\*.jpg')
        for file in image_files:
            image_id = re.search('(\d{8})', file).group(0).lstrip('0')
            file_name = re.search('(\d{8}.*?jpg)', file).group(0)
            image = cv2.imread(file)
            image_data.append(Epfl2DatasetImage(str(num), image_id, file_name, image))

    return image_data


def transfer_data(annotations, image_data):
    if len(annotations.keys()) != len(image_data):
        print('Annotation and Image count must match. '
                        'Annotation Count: ' + str(len(annotations.keys())) + ' image count: ' + str(len(image_data)))

    database = DatasetDBV2(DATASET_EPFL2)
    for key in annotations.keys():
        database.insert_annotation_data(annotations[key])

    for data in image_data:
        database.insert_image_data(data)


def run():
    labels_folder =\
        [
            ['person','gt_files242_person'],
            ['car','gt_files242_car'],
            ['bus','gt_files242_bus'],
        ]
    annotations = get_annotations(labels_folder)
    images = get_images(6, annotations.keys())
    transfer_data(annotations, images)


run()
