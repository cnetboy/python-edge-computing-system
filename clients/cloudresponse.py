
class CloudResponse(object):

    def __init__(self, classification, status, error_message=None):
        self.classification = classification
        self.status = status
        self.error_message = error_message

    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, classification):
        self.__classification = classification

    @property
    def error_message(self):
        return self.__error_message

    @error_message.setter
    def error_message(self, error_message):
        self.__error_message = error_message
