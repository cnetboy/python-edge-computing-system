from model.fasterrcnn import FasterRcnn
from model.yolov2tiny import YoloV2Tiny
from model.yolov2full import YoloV2Full
from processors.processor import Processor
from common.userparameters import UserParameters, MODEL_YOLOV2, MODEL_FASTERRCNN
from config.configadapters import NODE
from clients.generalresponse import GeneralResponse
import clients.responsestatus as status


def get_none_node_model():
    model = UserParameters().get_none_node_model()
    if model == MODEL_YOLOV2:
        return YoloV2Full()
    elif model == MODEL_FASTERRCNN:
        return FasterRcnn()


class RunModelProcessor(Processor):

    def process(self, request):
        component = UserParameters().get_component()
        response_code = status.ResponseStatus.SUCCESS

        if component == NODE:
            boxed_image, boxes = YoloV2Tiny().predict(request.request.image)
            request.request.set_prediction(boxes)
            response_code = status.ResponseStatus.CONTINUE
        else:
            boxed_image, boxes = get_none_node_model().predict(request.request.image)

        return GeneralResponse(response_code, boxed_image, boxes)
