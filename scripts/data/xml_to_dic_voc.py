import numpy as np
import xml.etree.ElementTree as ET


def generate_voc_format_dataset(xml_locs, source):
    dataset = list()
    filenames = list()
    for index, xml in enumerate(xml_locs):
        dataset_candidate = VOCFormatDataSet(xml, source)
        if dataset_candidate.get_file_name().__contains__('n02802426'):
            dataset.append(dataset_candidate)
            filenames.append(dataset_candidate.get_file_name())
    return filenames, dataset


class VOCFormatDataSet(object):

    def __init__(self, xml_loc, source):
        self.xml_map = create_xml_map(xml_loc)
        self.xml_map['image_id'] = self.get_file_name().replace('.jpg', '')
        self.xml_map['source'] = source

    def get_file_name(self):
        return self.xml_map['filename']

    def get_width(self):
        return self.xml_map['width']

    def set_width(self, width):
        self.xml_map['width'] = width

    def get_height(self):
        return self.xml_map['height']

    def set_height(self, height):
        self.xml_map['height'] = height

    def get_objects(self):
        return create_voc_objects(self.xml_map['object'])

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_dic(self):
        return self.xml_map


def create_xml_map(xml_loc):
    tree = ET.parse(xml_loc)
    xml_map = {'object':[]}
    xml_map['filename'] = tree.find('filename').text
    xml_map['width'] = int(tree.find('size').find('width').text)
    xml_map['height'] = int(tree.find('size').find('height').text)
    xml_obj_node = tree.findall('object')
    for obj_node in xml_obj_node:
        obj = {}
        obj['name'] = obj_node.find('name').text
        bnd_box = obj_node.find('bndbox')
        obj['xmin'] = float(bnd_box.find('xmin').text)
        obj['ymin'] = float(bnd_box.find('ymin').text)
        obj['xmax'] = float(bnd_box.find('xmax').text)
        obj['ymax'] = float(bnd_box.find('ymax').text)
        xml_map['object'] += [obj]

    return xml_map


def create_voc_objects(obj_xml_maps):
    voc_object = list()
    for obj_xml in obj_xml_maps:
        voc_object.append(VOCObject(obj_xml))
    return np.array(voc_object)


class VOCObject(object):

    def __init__(self, xml_map):
        self.xml_map = xml_map

    def get_name(self):
        return self.xml_map['name']

    def set_name(self, name):
        self.xml_map['name'] = name

    def get_bnd_box(self):
        return VOCBndBox(self.xml_map)


class VOCBndBox(object):

    def __init__(self, xml_map):
        self.xml_map = xml_map

    def get_xmin(self):
        return self.xml_map['xmin']

    def set_xmin(self, xmin):
        self.xml_map['xmin'] = xmin

    def get_ymin(self):
        return self.xml_map['ymin']

    def set_ymin(self, ymin):
        self.xml_map['ymin'] = ymin

    def get_xmax(self):
        return self.xml_map['xmax']

    def set_xmax(self, xmax):
        self.xml_map['xmax'] = xmax

    def get_ymax(self):
        return self.xml_map['ymax']

    def set_ymax(self, ymax):
        self.xml_map['ymax'] = ymax
