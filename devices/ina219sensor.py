from ina219 import INA219
from ina219 import DeviceRangeError


class INA219DCCurrentSensor(object):

    INA_SHUNT_OHMS = 0.1
    INA_MAX_AMPS = 2.0

    def __init__(self):
        self.ina = INA219(shunt_ohms=self.INA_SHUNT_OHMS, max_expected_amps=self.INA_MAX_AMPS)

    def get_voltage(self):
        try:
            return self.ina.shunt_voltage()
        except DeviceRangeError as e:
            return 0

    def get_current(self):
        try:
            return self.ina.current()
        except DeviceRangeError as e:
            return 0

    def get_power(self):
        try:
            return self.ina.power()
        except DeviceRangeError as e:
            return 0
