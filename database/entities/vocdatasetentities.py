from common.logger import get_logger
my_logger = get_logger(__name__)


class VocDatasetImage(object):

    def __init__(self, image_id, filename, image):
        self.image_id = image_id
        self.filename = filename
        self.image = image

    def get_image_id(self):
        return self.image_id

    def get_filename(self):
        return self.filename

    def get_image(self):
        return self.image


class VocDatasetAnnotation(object):

    def __init__(self, annotation_data):
        self.annotation_data = annotation_data

    def get_annotation(self):
        return self.annotation_data

    def get_dict(self):
        return self.annotation_data.get_dict()


class VocDatasetAnnotationDAO(object):

    def __init__(self, filename, width, height, image_id, source, objs):
        self.filename = filename
        self.width = width
        self.height = height
        self.image_id = image_id
        self.source = source
        self.objects = list()
        for obj in objs:
            objs.append(VocDatasetAnnotationObjectDAO(obj))

    def get_filename(self):
        return self.filename

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_image_id(self):
        return self.image_id

    def get_source(self):
        return self.source

    def get_objects(self):
        return self.objects


class VocDatasetAnnotationObjectDAO(object):

    def __init__(self, obj):
        self.name = obj['name']
        self.xmin = obj['xmin']
        self.ymin = obj['ymin']
        self.xmax = obj['xmax']
        self.ymax = obj['ymax']

    def get_name(self):
        return self.name

    def get_xmin(self):
        return self.xmin

    def get_ymin(self):
        return self.ymin

    def get_xmax(self):
        return self.xmax

    def get_ymax(self):
        return self.ymax


class VocDatasetLabel(object):

    def __init__(self, source, index, name):
        self.source = source
        self.index = index
        self.name = name

    def get_source(self):
        return self.source

    def get_index(self):
        return self.index

    def get_name(self):
        return self.name
