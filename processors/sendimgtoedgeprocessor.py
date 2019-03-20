from processors.processor import Processor

import clients.edgerequest as req
import clients.edgeclient as client


class SendImgToEdgeProcessor(Processor):

    def process(self, request):
        edge_request = req.EdgeRequest(None, request.request.image)
        return client.post_to_single_view(edge_request)
