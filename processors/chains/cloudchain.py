import processors.runmodelprocessor as run_model
import processors.runmultiviewprocessor as run_multi_view


class SingleViewChain(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.processor = run_model.RunModelProcessor(None)
        return cls._instance

    def get_processor(self):
        return self.processor


class MultiViewChain(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.processor = run_multi_view.RunMultiViewProcessor(None)
        return cls._instance

    def get_processor(self):
        return self.processor
