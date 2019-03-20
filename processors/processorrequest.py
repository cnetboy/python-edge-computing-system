

class ProcessorRequest(object):

    def __init__(self, request):
        self.request = request
        self.net_out = None

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    @property
    def net_out(self):
        return self.__net_out

    @net_out.setter
    def net_out(self, net_out):
        self.__net_out = net_out
