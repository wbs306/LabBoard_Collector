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
        for c in collectors:
            if (time.time() - c.last_collect < c.collect_interval):
                continue
            logging.info(f"Collecting data from {c.name}...")
            data = list(c.get_data().values())
            data.insert(0, "'" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'")
            database.write(c.name, data)
            c.last_collect = time.time()

        time.sleep(1)

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
                time.sleep(0.5)
                pass
        except KeyboardInterrupt:
            GlobalConfig.is_exit = True
            logging.info("Waiting, timer is closing the database...")
        finally:
            while (timer_thread.is_alive()):
                pass
        
        if (GlobalConfig.is_using_battery):
            subprocess.call(["shutdown", "now"])


if (__name__ == "__main__"):
    LBCollector().run()