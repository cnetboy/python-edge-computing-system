from model.multiviewdetector import MultiviewDetector
from processors.processor import Processor
from clients.generalresponse import GeneralResponse
import clients.responsestatus as status
from time import time as timer


class RunMultiViewProcessor(Processor):

    def process(self, request):
        response_code = status.ResponseStatus.SUCCESS
        start_time = timer()
        boxed_image, boxes = MultiviewDetector().predict(request.request.frame_num, request.request.cam_num, request.request.image)
        duration = str(timer() - start_time)
        print('Computational Time: ' + duration)
        return GeneralResponse(response_code, boxed_image, boxes, duration)
