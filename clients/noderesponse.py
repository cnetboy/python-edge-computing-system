
class NodeResponse(object):

    def __init__(self, status, boxed_image, boxed_loc=None, error_message=None):
        self.status = status
        self.boxed_image = boxed_image
        self.boxed_loc = boxed_loc
        self.error_message = error_message

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def boxed_image(self):
        return self.__boxed_image

    @boxed_image.setter
    def boxed_image(self, boxed_image):
        self.__boxed_image = boxed_image

    @property
    def boxed_loc(self):
        return self.__boxed_loc

    @boxed_loc.setter
    def boxed_loc(self, boxed_loc):
        self.__boxed_loc = boxed_loc

    @property
    def error_message(self):
        return self.__error_message

    @error_message.setter
    def error_message(self, error_message):
        self.__error_message= error_message
