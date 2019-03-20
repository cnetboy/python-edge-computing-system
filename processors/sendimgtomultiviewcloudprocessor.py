from processors.processor import Processor

import clients.cloudrequest as req
import clients.cloudclient as client


class SendImgToMultiViewCloudProcessor(Processor):

    def process(self, request):
        cloud_request = req.CloudRequest(request.request.image)
        client.post_to_multi_view(cloud_request)
