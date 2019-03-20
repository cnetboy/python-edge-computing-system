from common.observer import Observer
from processors.chains.commonchain import CHAIN_CONFIG_SINGLE_CLOUD, CHAIN_CONFIG_SINGLE_EDGE, CHAIN_CONFIG_MULTI_CLOUD, CHAIN_CONFIG_MULTI_EDGE
import processors.runmodelprocessor as run_model
import processors.sendimgtoedgeprocessor as send_to_edge
import processors.sendimgtocloudprocessor as send_to_cloud
import processors.sendimgtomultiviewedgeprocessor as send_to_multi_view_edge
import processors.sendimgtomultiviewcloudprocessor as send_to_multi_view_cloud


class CameraChain(Observer):
    _instance = None

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__new__(self, *args, **kwargs)
            self.processor = send_to_edge.SendImgToEdgeProcessor(None)
        return self._instance

    def get_processor(self):
        return self.processor

    def update(self, arg):
        if str(arg).upper().__contains__('NODE'):
            self.processor = run_model.RunModelProcessor(None)
        elif str(arg).upper() == CHAIN_CONFIG_SINGLE_CLOUD:
            self.processor = send_to_cloud.SendImgToCloudProcessor(None)
        elif str(arg).upper() == CHAIN_CONFIG_SINGLE_EDGE:
            self.processor = send_to_edge.SendImgToEdgeProcessor(None)
        elif str(arg).upper() == CHAIN_CONFIG_MULTI_CLOUD:
            self.processor = run_model.RunModelProcessor(send_to_multi_view_cloud.SendImgToMultiViewCloudProcessor(None))
        elif str(arg).upper() == CHAIN_CONFIG_MULTI_EDGE:
            self.processor = run_model.RunModelProcessor(send_to_multi_view_edge.SendImgToMultiViewEdgeProcessor(None))
        else:
            print("No processor change occurred. Invalid argument: " + str(arg))
