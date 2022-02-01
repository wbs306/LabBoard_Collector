import datetime
import logging
import os
import signal
import time
from threading import Thread
from xml.dom.minidom import parseString

import GlobalConfig
from DataWriter import DataWriter
from FanCollector import FanCollector
from UPSCollector import UPSCollector
from SensorCollector import SensorCollector

LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def timer(collectors, db_path, interval):
    if (not os.path.exists(db_path)):
        data_dicts = {}
        for c in collectors:
            data_dicts[c.name] = c.data_dict
        database = DataWriter(db_path, data_dicts)
    else:
        database = DataWriter(db_path)

    while (not GlobalConfig.is_exit):
        logging.info("Timer: Collecting data.")
        for c in collectors:
            data = list(c.get_data().values())
            data.insert(0, "'" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'")
            database.write(c.name, data)      

        time.sleep(interval)

    database.stop()

class LBCollector:
    def __init__(self, db_path):
        self.collectors = [
            FanCollector(),
            UPSCollector(),
            SensorCollector()
        ]

        self.collect_interval = 10
        self.database = db_path

    def run(self):
        logging.info("Starting collector threads.")
        threads = []
        for c in self.collectors:
            if (c.have_task):
                t = Thread(target=c.run_task, name=c.name)
                t.setDaemon(True)
                threads.append(t)
        for t in threads:
            t.start()

        timer_thread = Thread(target=timer, name="Timer", args=[self.collectors, self.database, self.collect_interval])
        time.sleep(1)
        logging.info("Starting timer thread.")
        timer_thread.setDaemon(True)
        timer_thread.start()
        threads.append(timer_thread)

        try:
            while (True):
                pass
        except KeyboardInterrupt:
            GlobalConfig.is_exit = True
            logging.info("Waiting, timer is closing the database...")
            while (timer_thread.isAlive()):
                pass


if (__name__ == "__main__"):
    LBCollector("test.db").run()