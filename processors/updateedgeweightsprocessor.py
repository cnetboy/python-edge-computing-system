from processors.processor import Processor

import clients.edgerequest as req
import clients.edgeclient as client


class UpdateEdgeWeightsProcessor(Processor):

    def process(self, request):
        edge_request = req.EdgeRequest(None, request.image)
        client.post_to_model_weight_update_service(edge_request)
