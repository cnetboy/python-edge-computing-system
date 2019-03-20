import glob
import cv2

from database.datasetdbv2 import DatasetDBV2, DATASET_VOC
from database.entities.vocdatasetentities import VocDatasetImage, VocDatasetLabel
from scripts.data.xml_to_dic_voc import generate_voc_format_dataset


def get_annotations(loc, source):
    xmls = glob.glob(loc + "*.xml")
    filenames, annotations = generate_voc_format_dataset(xmls, source)

    return filenames, annotations


def construct_image_fields(image_name, image_loc):
    image_id = str(image_name).replace('.jpg', '')
    filename = image_name
    image = cv2.imread(image_loc + image_name)
    return VocDatasetImage(image_id, filename, image)


def get_images(image_names, image_loc):
    image_data = list()

    for name in image_names:
        image_data.append(construct_image_fields(name, image_loc))

    return image_data


def transfer_data(annotations, image_data):
    if len(annotations) != len(image_data):
        raise Exception('Annotation and Image count must match. '
                        'Annotation Count: ' + str(len(annotations)) + ' image count: ' + str(len(image_data)))

    database = DatasetDBV2(DATASET_VOC)
    for annotation in annotations:
        database.insert_annotation_data(annotation)

    for data in image_data:
        database.insert_image_data(data)


def run():
    annotation_images_loc_2007 = \
        [
            "D:\\Files\\dataset\\voc\\VOCtrainval_06-Nov-2007\\VOCdevkit\\VOC2007\\Annotations\\",
            "D:\\Files\\dataset\\voc\\VOCtrainval_06-Nov-2007\\VOCdevkit\\VOC2007\\JPEGImages\\",
            "VOC2007"
        ]

    annotation_images_loc_2012 = \
        [
            "D:\\Files\\dataset\\voc\\VOCtrainval_11-May-2012\\VOCdevkit\\VOC2012\\Annotations\\",
            "D:\\Files\\dataset\\voc\\VOCtrainval_11-May-2012\\VOCdevkit\\VOC2012\\JPEGImages\\",
            "VOC2012"
        ]

    data_info = list()
    data_info.append(annotation_images_loc_2007)
    data_info.append(annotation_images_loc_2012)
    for info in data_info:
        filenames, annotations = get_annotations(info[0], info[2])
        image_data = get_images(filenames, info[1])
        transfer_data(annotations, image_data)


#run()

CLASS_DIC =\
    {
        "background": 0,
        "aeroplane": 1,
        "bicycle": 2,
        "bird": 3,
        "boat": 4,
        "bottle": 5,
        "bus": 6,
        "car": 7,
        "cat": 8,
        "chair": 9,
        "cow": 10,
        "diningtable": 11,
        "dog": 12,
        "horse": 13,
        "motorbike": 14,
        "person": 15,
        "pottedplant": 16,
        "sheep": 17,
        "sofa": 18,
        "train": 19,
        "tvmonitor": 20,
        "unknown": 21,
    }


def set_labels():
    labels = list()
    for key in CLASS_DIC.keys():
        labels.append(VocDatasetLabel("VOC", CLASS_DIC[key], key))

    database = DatasetDBV2(DATASET_VOC)
    for label in labels:
        database.insert_label_names(label)

set_labels()
