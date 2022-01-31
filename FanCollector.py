import RPi.GPIO as gpio
import logging
import time

from Collector import Collector

class FanCollector(Collector):
    def __init__(self):
        super().__init__("FanCollector")

        # Fan GPIO Pin
        self._FAN_GPIO = 12

        # Start the fan when CPU temperature hit TEMP_MIN
        self._TEMP_MIN = 30

        # Full running the fan when CPU temperature hit TEMP_MAX
        self._TEMP_MAX = 50

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self._FAN_GPIO, gpio.OUT)

        # The frequency of PWM
        self._pwm_freq = 75
        self._pwm = gpio.PWM(self._FAN_GPIO, self._pwm_freq)
        self._pwm.start(0)

        # To check the CPU temperature per _check_interval second
        self._check_interval = 15
        self._fan_speed = 0
        self._cpu_temp = 0

    def run_task(self):
        logging.info(f"{self.name} started.")
        while (True):
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
