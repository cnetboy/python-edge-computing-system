

class DeviceInfo(object):

    def __init__(self, ip):
        self.ip = ip
        self.battery_life = None
        self.comp_time = None
        self.comp_loc = 'EDGE'

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def battery_life(self):
        return self.__battery_life

    @battery_life.setter
    def battery_life(self, battery_life):
        self.__battery_life = battery_life

    @property
    def comp_time(self):
        return self.__comp_time

    @comp_time.setter
    def comp_time(self, comp_time):
        self.__comp_time = comp_time

    @property
    def comp_loc(self):
        return self.__comp_loc

    @comp_time.setter
    def comp_loc(self, comp_loc):
        self.comp_loc = comp_loc
