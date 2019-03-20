
class NodeRequest(object):

    def __init__(self, image=None, cam=1, frame=1, prediction=None, weights=None):
        self.image = image
        self.cam = cam
        self.frame = frame
        self.prediction = prediction
        self.weights = weights

    def image(self):
        return self.image

    def cam(self):
        return self.cam

    def frame(self):
        return self.frame

    def set_prediction(self, prediction):
        self.prediction = prediction

    def prediction(self):
        return self.prediction

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, weights):
        self.__weights = weights
