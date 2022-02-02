import RPi.GPIO as gpio
import logging
import time

import GlobalConfig
from Collector import Collector

class FanCollector(Collector):
    def __init__(self):
        super().__init__("FanCollector")
        self.data_dict = {
            "cpu_temp": "FLOAT",
            "fan_speed": "FLOAT"
        }

        self._FAN_GPIO = GlobalConfig.fan_gpio
        self._TEMP_MIN = GlobalConfig.temp_min
        self._TEMP_MAX = GlobalConfig.temp_max

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self._FAN_GPIO, gpio.OUT)

        self._pwm_freq = GlobalConfig.pwm_freq
        self._pwm = gpio.PWM(self._FAN_GPIO, self._pwm_freq)
        self._pwm.start(0)

        # To check the CPU temperature per _check_interval second
        self._check_interval = GlobalConfig.check_interval
        self._fan_speed = 0
        self._cpu_temp = 0

    def run_task(self):
        logging.info(f"{self.name} started.")
        while (GlobalConfig.is_exit):
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                self._cpu_temp = float(f.read())
            if self._cpu_temp < self._TEMP_MIN * 1000:
                self._pwm.stop()
                self._fan_speed = 0
            elif self._cpu_temp > self._TEMP_MAX * 1000:
                self._pwm.start(100)
                self._fan_speed = 100
            else:
                dc = (self._cpu_temp - self._TEMP_MIN * 1000) * 100 / ((self._TEMP_MAX - self._TEMP_MIN) * 1000)
                self._pwm.start(dc)
                self._fan_speed = dc
            time.sleep(self._check_interval)
        gpio.cleanup()

    def get_data(self):
        return {
            "cpu_temp": self._cpu_temp,
            "fan_speed": self._fan_speed
        }
