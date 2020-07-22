#! /usr/bin/evn python
from daemon_base import Daemon

from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert
import sensor
import datetime
import logging
import time

def insert_data(engine):
    with engine.connect() as conn:
        meta = MetaData()
        wp = Table('weather_param', meta, autoload=True, autoload_with=conn)
        # print(meta.tables)
        t, h, p = sensor.bme280.temperature, sensor.bme280.humidity, sensor.bme280.pressure
        st = insert(wp).values(temperature=t,
                               humidity=h, 
                               pressure=p,
                               record_time=datetime.datetime.now())
        conn.execute(st)
    return t, h, p

class DataCollectorDaemon(Daemon):
    
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', interval=10):
        super().__init__(pidfile, stdin, stdout, stderr)
        self.interval = interval

    def run(self):
       
        logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
        logging.info("Collecting process started...")

        engine = create_engine("postgresql:///weather")

        while True:
            ret = insert_data(engine)
            logging.info(str(ret))
            time.sleep(self.interval)

if __name__ == "__main__":
    pass