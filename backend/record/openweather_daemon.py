#! /usr/bin/evn python
from daemon_base import Daemon

from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert

import datetime
import time
import sys
import requests


API_KEY_FILE="./apikey.json"
CITY="Shanghai"

# See the apidoc in https://openweathermap.org/current
URL="https://api.openweathermap.org/data/2.5/weather?q=${cityname}&appid=${apikey}"

SQL_CONN_STR = "postgresql:///weather"

class OpenWeatherDaemon(Daemon):

    def __init__(self, pidfile, interval):
        super().__init__(pidfile)
        self.interval = interval
    
    def run(self):
        self.log.info("Weather collecting process started...")
        engine = create_engine(SQL_CONN_STR)

        while True:
            # ret = insert_data(engine)
            # self.log.info(str(ret))
            time.sleep(self.interval)

if __name__ == "__main__":
    pass