import datetime

DATA_TYPE_COMPUTING_TIME = "COMPUTING TIME (Seconds)"
DATA_TYPE_PROCESSING_TIME = "PROCESSING TIME (Seconds)"
DATA_TYPE_DATA_TRANSFER_TIME = "DATA TRANSFER TIME (Seconds)"
DATA_TYPE_TRANSFER_SIZE = "TRANSFER SIZE (Bytes)"
DATA_TYPE_FPS = "FPS"
DATA_TYPE_DETECTION = "DETECTION"


class DataCollector(object):
    _instance = None

    def __new__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__new__(self, *args, **kwargs)
            current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            self.file_name = 'data_collected_' + current_time
            self.fd = open(self.file_name, 'w+')
        return self._instance

    def write(self, data_type, data):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.fd.write(current_time + ' || ' + data_type + " :: " + data + '\n')

    def close(self):
        self.fd.close()
