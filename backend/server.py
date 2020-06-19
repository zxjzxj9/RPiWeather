#! /usr/bin/env python

""" Srcipt to launch a flask server
    Authored by Victor Zhang, 06/12/2020
"""

from flask import Flask, request
from weather_restful import app
import argparse


parser = argparse.ArgumentParser(description='Flask data RESTful server')
parser.add_argument("-b", "--host", type=str, default="0.0.0.0", help="Binding host")
parser.add_argument("-p", "--port", type=int, default=8080, help="Binding port")
parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
args = parser.parse_args()

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=args.debug)
