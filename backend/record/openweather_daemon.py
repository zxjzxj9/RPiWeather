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
                    weather_id = data["weather"]["id"],
                    weather_main = data["weather"]["main"],
                    weather_description = data["weather"]["description"],
                    weather_icon = data["weather"]["icon"],
                    base = data["base"],
                    main_temp = data["main"]["temp"],
                    main_feels_like = data["main"]["feels_like"],
                    main_temp_min = data["main"]["temp_min"],
                    main_temp_max = data["main"]["temp_max"],
                    main_pressure = data["main"]["pressure"],
                    main_humidity = data["main"]["humidity"],
                    visibility = data["visibility"],
                    wind_speed = data["wind"]["speed"],
                    wind_deg = data["wind"]["deg"],
                    clouds_all = data["clouds"]["all"],
                    dt = data["dt"],
                    sys_type = data["sys"]["type"],
                    sys_id = data["sys"]["id"],
                    sys_country = data["sys"]["country"],
                    sys_sunrise = data["sys"]["sunrise"],
                    sys_sunset = data["sys"]["sunset"],
                    timezone = data["timezone"],
                    id = data["id"],
                    name = data["name"],
                    cod = data["cod"]
                )

        except Exception as e:
            self.log.error(e)
    
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