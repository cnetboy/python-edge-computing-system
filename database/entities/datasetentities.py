from common.logger import get_logger
my_logger = get_logger(__name__)


class DatasetEntity(object):

    def __init__(self, images, labels):
        if len(images) != len(labels):
            raise Exception("Images and Labels count must match.")
        self.images = images
        self.labels = labels

    def get_images(self):
        return self.images

    def get_labels(self):
        return self.labels

    def __len__(self):
        return len(self.labels)


class DatasetImage(object):

    def __init__(self, image_id, filename, image):
        self.image_id = image_id
        self.filename = filename
        if image.shape != (32, 32, 3):
            image = image.reshape((3, 32, 32)).transpose(1, 2, 0)
        self.image = image

    def get_image_id(self):
        return self.image_id

    def get_filename(self):
        return self.filename

    def get_image(self):
        return self.image


class DatasetLabel(object):

    def __init__(self, image_id, source, _type, label):
        self.image_id = image_id
        self.source = source
        self.type = _type
        self.label = label

    def get_image_id(self):
        return self.image_id

    def get_source(self):
        return self.source

    def get_type(self):
        return self.type

    def get_label(self):
        return self.label


class DatasetLabelName(object):

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
