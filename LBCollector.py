import datetime
import logging
import os
import subprocess
import time
from threading import Thread

import GlobalConfig
from DataWriter import DataWriter
from FanCollector import FanCollector
from UPSCollector import UPSCollector
from SensorCollector import SensorCollector

LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def timer(collectors):
    db_path = GlobalConfig.db_path
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

        time.sleep(GlobalConfig.collect_interval)

    database.stop()

class LBCollector:
    def __init__(self):
        self.collectors = [
            FanCollector(),
            UPSCollector(),
            SensorCollector()
        ]

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

        timer_thread = Thread(target=timer, name="Timer", args=[self.collectors])
        time.sleep(1)
        logging.info("Starting timer thread.")
        timer_thread.setDaemon(True)
        timer_thread.start()
        threads.append(timer_thread)

        try:
            while (not GlobalConfig.is_exit):
                pass
        except KeyboardInterrupt:
            GlobalConfig.is_exit = True
            logging.info("Waiting, timer is closing the database...")
        finally:
            while (timer_thread.isAlive()):
                pass
        
        if (GlobalConfig.is_using_battery):
            subprocess.call(["shutdown", "now"])


if (__name__ == "__main__"):
    LBCollector().run()