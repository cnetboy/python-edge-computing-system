from processors.processor import Processor

import clients.noderequest as req
import clients.nodeclient as client


class UpdateNodeWeightsProcessor(Processor):

    def process(self, request):
        noded_request = req.NodeRequest(request.image)
        client.post_to_model_weight_update_service(noded_request)
