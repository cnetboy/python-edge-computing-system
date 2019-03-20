
class AnnotationFindBuilder(object):

    def __init__(self):
        self.find_query = dict()

    def build_image_id(self, imageId):
        self.find_query['image_id'] = imageId

    def build_image_id_gte_lte(self, gte_id, lte_id):
        self.find_query['image_id'] = {'$gte': gte_id, '$lte': lte_id}

    def build_source(self, source):
        self.find_query['source'] = source

    def build_type(self, typeOfData):
        self.find_query['type'] = typeOfData

    def build_label(self, label):
        self.find_query['label'] = label

    def build_result_columns(self, columns, no_id=True):
        if len(self.find_query) > 1:
            raise Exception("Restriction added already.")

        column_dict = dict()
        for column in columns:
            column_dict[column] = 1

        if no_id:
            column_dict['_id'] = 0

        self.find_query = self.find_query, column_dict

    def build(self):
        return self.find_query


class ImageFindBuilder(object):

    def __init__(self):
        self.find_query = dict()

    def build_image_id(self, imageId):
        self.find_query['image_id'] = imageId

    def build_image_id_gte_lte(self, gte_id, lte_id):
        self.find_query['image_id'] = {'$gte': gte_id, '$lte': lte_id}

    def build_filename(self, filename):
        self.find_query['filename'] = filename

    def build_result_columns(self, columns, no_id=True):
        if len(self.find_query) > 1:
            raise Exception("Restriction added already.")

        column_dict = dict()
        for column in columns:
            column_dict[column] = 1

        if no_id:
            column_dict['_id'] = 0

        self.find_query = self.find_query, column_dict

    def build(self):
        return self.find_query


class LabelFindBuilder(object):

    def __init__(self):
        self.find_query = dict()

    def build_index(self, index):
        self.find_query['index'] = index

    def build_index_id_gte_lte(self, gte_id, lte_id):
        self.find_query['index'] = {'$gte': gte_id, '$lte': lte_id}

    def build_source(self, source):
        self.find_query['source'] = source

    def build_name(self, name):
        self.find_query['name'] = name

    def build_result_columns(self, columns, no_id=True):
        if len(self.find_query) > 1:
            raise Exception("Restriction added already.")

        column_dict = dict()
        for column in columns:
            column_dict[column] = 1

        if no_id:
            column_dict['_id'] = 0

        self.find_query = self.find_query, column_dict

    def build(self):
        return self.find_query
