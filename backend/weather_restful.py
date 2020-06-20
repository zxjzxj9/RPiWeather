#! /usr/bin/env python

from flask import Flask
from flasgger import Swagger
from flask_restful import Api, Resource
from resources import Example, DateWeather

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'Weather Forcast API System',
    'version': '0.0.1'.
    'uiversion': 3
}
swagger = Swagger(app)

api.add_resource(Example, '/example')
api.add_resource(DateWeather, '/date_weather')
