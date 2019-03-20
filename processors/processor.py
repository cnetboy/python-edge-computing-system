from abc import ABCMeta, abstractmethod
from clients.noderesponse import NodeResponse
from clients.responsestatus import ResponseStatus


class Processor(metaclass=ABCMeta):

    def __init__(self, successor=None):
        self._successor = successor

    def run(self, request):
        response = self.process(request)

        if response.status == ResponseStatus.SUCCESS:
            return response

        if self._successor:
            return self._successor.run(request)
        else:
            return NodeResponse(ResponseStatus.ERROR, request.request.image)

    @abstractmethod
    def process(self, request):
        pass
