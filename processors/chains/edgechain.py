from processors.chains.commonchain import CHAIN_CONFIG_SINGLE_CLOUD, CHAIN_CONFIG_SINGLE_EDGE, CHAIN_CONFIG_MULTI_CLOUD, CHAIN_CONFIG_MULTI_EDGE
from common.observer import Observer
import processors.runmodelprocessor as run_model
import processors.runmultiviewprocessor as run_multi_view
import processors.sendimgtocloudprocessor as send_to_cloud
import processors.sendimgtomultiviewcloudprocessor as send_to_multi_view_cloud


class SingleViewChain(Observer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.processor = run_model.RunModelProcessor(send_to_cloud.SendImgToCloudProcessor(None))
        return cls._instance

    def get_processor(self):
        return self.processor

    def update(self, arg):
        if str(arg).upper().__contains__('MULTI'):
            return

        if str(arg).upper() == CHAIN_CONFIG_SINGLE_CLOUD:
            self.processor = send_to_cloud.SendImgToCloudProcessor(None)
        elif str(arg).upper() == CHAIN_CONFIG_SINGLE_EDGE:
            self.processor = run_model.RunModelProcessor(None)
        else:
            print("No processor change occurred. Invalid argument: " + str(arg))


class MultiViewChain(Observer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.processor = run_multi_view.RunMultiViewProcessor(None)
        return cls._instance

    def get_processor(self):
        return self.processor

    def update(self, arg):
        if str(arg).upper().__contains__('SINGLE'):
            return
        if str(arg).upper() == CHAIN_CONFIG_MULTI_CLOUD:
            self.processor = send_to_multi_view_cloud.SendImgToMultiViewCloudProcessor(None)
        elif str(arg).upper() == CHAIN_CONFIG_MULTI_EDGE:
            self.processor = run_multi_view.RunMultiViewProcessor(None)
        else:
            print("No processor change occurred. Invalid argument: " + str(arg))
