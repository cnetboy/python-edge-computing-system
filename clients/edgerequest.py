
class EdgeRequest(object):

    def __init__(self, ip, image=None, frame_num=1, cam_num=1, predicted_box_loc=None, boxed_image=None, weights=None):
        self.ip = ip
        self.image = image
        self.frame_num = int(frame_num)
        self.cam_num = int(cam_num)
        self.predicted_box_loc = predicted_box_loc
        self.boxed_image = boxed_image
        self.weights = weights

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    def frame_num(self):
        return self.frame_num

    def cam_num(self):
        return self.cam_num

    @property
    def predicted_box_loc(self):
        return self.__predicted_box_loc

    @predicted_box_loc.setter
    def predicted_box_loc(self, predicted_box_loc):
        self.__predicted_box_loc = predicted_box_loc

    @property
    def boxed_image(self):
        return self.__boxed_image

    @boxed_image.setter
    def boxed_image(self, boxed_image):
        self.__boxed_image = boxed_image

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, weights):
        self.__weights = weights

