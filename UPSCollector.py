import logging
import time

import GlobalConfig
from GlobalConfig import UPSCollectorConfig
from Collector import Collector
from INA219 import  INA219

class UPSCollector(Collector):
    def __init__(self):
        super().__init__("UPSCollector")
        self.data_dict = {
            "voltage": "FLOAT",
            "current": "FLOAT",
            "power": "FLOAT"
        }

        self._ina219 = INA219(addr=0x42)

        self._bus_voltage = self._ina219.getBusVoltage_V()
        self._current = self._ina219.getCurrent_mA()
        self._power = self._ina219.getPower_W()

    def run_task(self):
        logging.info(f"{self.name} started.")
        while (not GlobalConfig.is_exit):
            self._bus_voltage = self._ina219.getBusVoltage_V()
            self._current = self._ina219.getCurrent_mA() / 1000
            self._power = self._ina219.getPower_W()
            p = (self._bus_voltage - 6)/2.4*100
            if (p > 100):p = 100
            if (p < 0):p = 0

            if (self._current < -0.2):
                GlobalConfig.is_exit = True

            time.sleep(UPSCollectorConfig.battery_check_interval)

    def get_data(self):
        return {
            "voltage": self._bus_voltage,
            "current": self._current,
            "power": self._power
        }