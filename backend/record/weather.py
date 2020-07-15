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

def get_current_weather():
    pass