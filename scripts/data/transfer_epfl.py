import cv2
import json

from database.datasetdbv2 import DatasetDBV2, DATASET_EPFL
from database.entities.epfldatasetentities import EpflDatasetAnnotationObject, EpflDatasetAnnotation, EpflDatasetImage

ANNOTATION_LOCATION = 'D:\\Files\\BigFiles\\EPFL-RLC_dataset\\EPFL-RLC_dataset\\mv_examples\\positive.json'
IMAGE_BASE_LOCATION = 'D:\\Files\\BigFiles\\EPFL-RLC_dataset\\EPFL-RLC_dataset\\frames\\'


def get_annotations():
    with open(ANNOTATION_LOCATION, 'r') as f:
        annotations = json.load(f)

    ann_dict = dict()
    for annotation in annotations:
        if len(annotation['views']) != 3:
            raise Exception("There must be 3 annotation for each cam.")

        image_file = annotation['views'][0]['imageFile'].replace('cam0/', '').replace('cam1/', '').replace('cam2/', '').replace('C0', '').replace('C1', '').replace('C2', '')
        image_file2 = annotation['views'][1]['imageFile'].replace('cam0/', '').replace('cam1/', '').replace('cam2/', '').replace('C0', '').replace('C1', '').replace('C2', '')
        image_file3 = annotation['views'][2]['imageFile'].replace('cam0/', '').replace('cam1/', '').replace('cam2/', '').replace('C0', '').replace('C1', '').replace('C2', '')

        if (image_file != image_file2) or (image_file != image_file3):
            raise Exception("All must refer to same image.")

        anns = [None for _ in range(len(annotation['views']))]
        for cam_index, ann in enumerate(annotation['views']):
            ann_obj = EpflDatasetAnnotationObject('person', ann['xmin'], ann['ymin'], ann['xmax'], ann['ymax'])
            ann = EpflDatasetAnnotation(image_file.replace('-', '-C' + str(cam_index)), cam_index, 480, 270, image_file.replace('-', '-C' + str(cam_index)).replace('.jpeg', ''), 'EPFL', ann_obj)
            anns[cam_index] = ann

        if image_file not in ann_dict:
            ann_dict[image_file] = anns
        else:
            for index, ann in enumerate(anns):
                ann_dict[image_file][index].add_object(ann.get_objects()[0])
    return ann_dict


def construct_image_fields(image_name, image_loc):
    image_id = str(image_name).replace('.jpeg', '')
    filename = image_name
    image = cv2.imread(image_loc + image_name)
    return EpflDatasetImage(image_id, filename, image)


def get_images(image_names):
    image_data = list()

    for name in image_names:
        for cam_index in range(3):
            image_data.append(construct_image_fields(name.replace('-', '-C' + str(cam_index)), IMAGE_BASE_LOCATION + 'cam' + str(cam_index) + '\\'))

    return image_data


def transfer_data(annotations, image_data):
    if len(annotations)*3 != len(image_data):
        raise Exception('Annotation and Image count must match. '
                        'Annotation Count: ' + str(len(annotations)) + ' image count: ' + str(len(image_data)))

    database = DatasetDBV2(DATASET_EPFL)
    for key in annotations:
        for annotation_cam in annotations[key]:
            database.insert_annotation_data(annotation_cam)

    for data in image_data:
        database.insert_image_data(data)

def run():
    annotations = get_annotations()
    images = get_images(annotations.keys())
    transfer_data(annotations, images)

run()
