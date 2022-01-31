import logging
import time
from threading import Thread

from FanCollector import FanCollector
from UPSCollector import UPSCollector
from SensorCollector import SensorCollector

LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def timer(collectors, database, interval):
    while (True):
        logging.info("Timer: Collecting data.")
        for c in collectors:
            data = c.get_data()
            print(data)

        time.sleep(interval)

class LBCollector:
    def __init__(self):
        self.collectors = [
            FanCollector(),
            UPSCollector(),
            SensorCollector()
        ]

        self.collect_interval = 10
        self.database = None

    def run(self):
        logging.info("Starting collector threads.")
        threads = []
        for c in self.collectors:
            if (c.have_task):
                threads.append(Thread(target=c.run_task, name=c.name))
        for t in threads:
            t.start()

        timer_thread = Thread(target=timer, name="Timer", args=[self.collectors, self.database, self.collect_interval])
        time.sleep(1)
        logging.info("Starting timer thread.")
        timer_thread.start()
        threads.append(timer_thread)
        
        for t in threads:
            t.join()


if (__name__ == "__main__"):
    LBCollector().run()