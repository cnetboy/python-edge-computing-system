from common.logger import get_logger
my_logger = get_logger(__name__)


class Epfl2DatasetImage(object):

    def __init__(self, cam_num, image_id, filename, image):
        self.cam_num = cam_num
        self.image_id = image_id
        self.filename = filename
        self.image = image

    def get_cam_num(self):
        return self.cam_num

    def get_image_id(self):
        return self.image_id

    def get_filename(self):
        return self.filename

    def get_image(self):
        return self.image


class Epfl2DatasetAnnotationObject(object):

    def __init__(self, name, xmin, ymin, xmax, ymax):
        self.name = name
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)

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


class Epfl2DatasetAnnotation(object):

    def __init__(self, filename, cam_num, width, height, image_id, source, obj):
        self.filename = filename
        self.cam_num = cam_num
        self.width = width
        self.height = height
        self.image_id = image_id
        self.source = source
        self.object = list()
        if isinstance(obj, list):
            for o in obj:
                self.object.append(o)
        else:
            self.object.append(obj)

    def get_filename(self):
        return self.filename

    def get_cam_num(self):
        return self.cam_num

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_image_id(self):
        return self.image_id

    def get_source(self):
        return self.source

    def get_objects(self):
        return self.object

    def add_object(self, obj):
        self.object.append(obj)

    def get_dict(self):
        dict = self.__dict__
        objects = [obj.__dict__ for obj in self.get_objects()]
        dict['object'] = objects
        return dict


class Epfl2DatasetLabel(object):

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
