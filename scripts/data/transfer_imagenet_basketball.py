import glob
import cv2

from database.datasetdbv2 import DatasetDBV2, DATASET_IMAGENET
from database.entities.imagenetdatasetentities import ImagenetDatasetImage, ImagenetDatasetLabel
from scripts.data.xml_to_dic_voc import generate_voc_format_dataset


def get_annotations(loc, source):
    xmls = glob.glob(loc + "*.xml")
    filenames, annotations = generate_voc_format_dataset(xmls, source)
    for annotation in annotations:
        for obj in annotation.get_objects():
            if obj.get_name() == 'n02802426':
                obj.set_name('basketball')
            else:
                obj.set_name('unknown')

    return filenames, annotations


def construct_image_fields(image_name, image_loc):
    image = cv2.imread(image_loc + image_name + '.JPEG')
    if image is None:
        return None
        #raise Exception('Invalid image file: ' + str(image_name))
    return ImagenetDatasetImage(image_name, image_name, image)


def get_images(image_names, image_loc):
    image_data = list()
    invalid_image_data = list()

    for name in image_names:
        image_candidate = construct_image_fields(name, image_loc)
        if image_candidate is None:
            invalid_image_data.append(name)
        else:
            image_data.append(image_candidate)

    return image_data, invalid_image_data


def transfer_data(annotations, image_data):
    if len(annotations) != len(image_data):
        raise Exception('Annotation and Image count must match. '
                        'Annotation Count: ' + str(len(annotations)) + ' image count: ' + str(len(image_data)))

    database = DatasetDBV2(DATASET_IMAGENET)
    for annotation in annotations:
        database.insert_annotation_data(annotation)

    for data in image_data:
        database.insert_image_data(data)


def run():
    imagenet_data = \
        [
            "D:\\Files\\dataset\\imagenet\\single\\basketball\\annotations\\",
            "D:\\Files\\dataset\\imagenet\\single\\basketball\\images\\",
            "IMAGENET"
        ]

    data_info = list()
    data_info.append(imagenet_data)
    for info in data_info:
        filenames, annotations = get_annotations(info[0], info[2])
        image_data, invalid_image_data = get_images(filenames, info[1])
        annotations_new = [x for x in annotations if x.get_file_name() not in invalid_image_data]
        transfer_data(annotations_new, image_data)

run()

# CLASS_DIC =\
#     {
#         "basketball": 22,
#     }
#
#
# def set_labels():
#     labels = list()
#     for key in CLASS_DIC.keys():
#         labels.append(ImagenetDatasetLabel("IMAGENET", CLASS_DIC[key], key))
#
#     database = DatasetDBV2(DATASET_IMAGENET)
#     for label in labels:
#         database.insert_label_names(label)
#
# set_labels()
