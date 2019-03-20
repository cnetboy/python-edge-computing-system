from processors.processor import Processor

import clients.edgerequest as req
import clients.edgeclient as client


class SendImgToMultiViewEdgeProcessor(Processor):

    def process(self, request):
        edge_request = req.EdgeRequest(None, request.request.image, request.request.frame, request.request.cam, request.request.prediction)
        return client.post_to_multi_view(edge_request)
