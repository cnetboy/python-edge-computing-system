from processors.processor import Processor

import clients.cloudrequest as req
import clients.cloudclient as client


class SendImgToCloudProcessor(Processor):

    def process(self, request):
        cloud_request = req.CloudRequest(None, request.request.image)
        return client.post_to_single_view(cloud_request)
