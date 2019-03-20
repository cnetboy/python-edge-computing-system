

class DeviceCache(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.devices = list()
        return self._instance

    @property
    def devices(self):
        return self.__devices

    @devices.setter
    def devices(self, devices):
        self.__devices = devices

    def append_device(self, device):
        self.devices.append(device)

    def remove_device(self, device_id):
        self.devices.remove(device_id)
