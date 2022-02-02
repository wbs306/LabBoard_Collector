import smbus
import time

from Collector import Collector
from GlobalConfig import SensorCollectorConfig

class SensorCollector(Collector):
    def __init__(self):
        super().__init__("SensorCollector", False)
        self.data_dict = {
            "temperature": "FLOAT",
            "humidity": "FLOAT"
        }

        # Get I2C bus
        self._bus = smbus.SMBus(1)

        self.collect_interval = SensorCollectorConfig.collect_interval

    # We don't need this
    def run_task(self):
        pass

    def get_data(self):
        # SHT30 address, 0x44(68)
        # Send measurement command, 0x2C(44)
        #		0x06(06)	High repeatability measurement
        self._bus.write_i2c_block_data(0x44, 0x2C, [0x06])

        time.sleep(0.5)
        
        # SHT30 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes
        # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self._bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temperature = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return {
            "temperature": temperature,
            "humidity": humidity
        }