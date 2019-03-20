
class GeneralResponse(object):

    def __init__(self, status, boxed_image, boxed_loc=None, error_message=None, computational_time=None, cam_num=None, frame_num=None, ):
        self.status = status
        self.boxed_image = boxed_image
        self.boxed_loc = boxed_loc
        self.error_message = error_message
        self.computational_time = computational_time
        self.cam_num = cam_num
        self.frame_num = frame_num

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
    def cam_num(self):
        return self.__cam_num

    @cam_num.setter
    def cam_num(self, cam_num):
        self.__cam_num = cam_num

    @property
    def frame_num(self):
        return self.__frame_num

    @frame_num.setter
    def frame_num(self, frame_num):
        self.__frame_num = frame_num

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

    @property
    def computational_time(self):
        return self.__computational_time

    @error_message.setter
    def computational_time(self, computational_time):
        self.__computational_time = computational_time
