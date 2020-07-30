#! /usr/bin/evn python
from daemon_base import Daemon

from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert
import sensor
import datetime
import time
import sys

SQL_CONN_STR = "postgresql:///weather"

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
    
    def __init__(self, pidfile, interval):
        super().__init__(pidfile)
        self.interval = interval

    def run(self):
       
        self.log.info("Collecting process started...")
        engine = create_engine(SQL_CONN_STR)

        while True:
            ret = insert_data(engine)
            self.log.info(str(ret))
            time.sleep(self.interval)

if __name__ == "__main__":
    pidf = "sensor.pid"
    dc = DataCollectorDaemon(pidf, 600)

    if sys.argv[1] == "start":
        dc.start()
    elif sys.argv[1] == "stop":
        dc.stop()
    elif sys.argv[1] == "restart":
        dc.restart()
    else:
        print("Unknown command: ", sys.argv[1])