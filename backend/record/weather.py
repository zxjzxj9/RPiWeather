#! /usr/bin/env python
""" This script is used to download the weather from website
    https://openweathermap.org
    You need an apikey.json file in the same folder, the format:
    {
        "apikey": "Your API Key"
    }
"""

import json
import requests

API_KEY_FILE="./apikey.json"

# See the apidoc in https://openweathermap.org/current
URL="https://api.openweathermap.org/data/2.5/weather?q=${cityname}&appid=${apikey}"

def get_current_weather():
    with open(API_KEY_FILE, "r") as apif:
        apikey = json.load(apif)["apikey"]
