#! /usr/bin/evn python
from daemon_base import Daemon

from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert

import datetime
import time
import sys
import requests
import string
import json

API_KEY_FILE="./apikey.json"
CITY="Shanghai"

# See the apidoc in https://openweathermap.org/current
URL="https://api.openweathermap.org/data/2.5/weather?q=${cityname}&appid=${apikey}"

SQL_CONN_STR = "postgresql:///weather"


class OpenWeatherDaemon(Daemon):

    def __init__(self, pidfile, interval):
        super().__init__(pidfile)
        self.interval = interval
        with open(API_KEY_FILE, "r") as apif:
            self.apikey = json.load(apif)["apikey"]

        self.url = string.Template(URL).substitute({
                "cityname": CITY,
                "apikey": self.apikey
            })
        self.engine = create_engine(SQL_CONN_STR)

    def get_current_weather(self):
<<<<<<< HEAD
        try:
            ret = requests.get(self.url)
            data = ret.json()

            with self.engine.connect() as conn:
                meta = MetaData()
                wdp = Table('weather_request', meta, autoload=True, autoload_with=conn)

                st = insert(wdp).values(
                    requests_time = datetime.datetime.now(),
                    coord_lon = data["coord"]["lon"],
                    coord_lat = data["coord"]["lat"],
                )

        except Exception as e:
            self.log.error(e)
=======
        ret = requests.get(self.url)
        data = ret.json()

        with self.engine.connect() as conn:
            meta = MetaData()
            wdp = Table('weather_request', meta, autoload=True, autoload_with=conn)
            
>>>>>>> a207f65d18f0998b18675b22463fda7754bd67cc
    
    def run(self):
        self.log.info("Weather collecting process started...")

        while True:
            # ret = insert_data(engine)
            # self.log.info(str(ret))
            time.sleep(self.interval)

if __name__ == "__main__":

    pidf = "weather.pid"
    owd = OpenWeatherDaemon(pidf, 3600)

    if sys.argv[1] == "start":
        owd.start()
    elif sys.argv[1] == "stop":
        owd.stop()
    elif sys.argv[1] == "restart":
        owd.restart()
    else:
        print("Unknown command: ", sys.argv[1])