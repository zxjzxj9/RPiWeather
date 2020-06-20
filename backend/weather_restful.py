#! /usr/bin/env python

from flask import Flask
from flasgger import Swagger
from flask_restful import Api, Resource
from resources import Example, DateWeather
from server_db import Session, TableList
import flask

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'Weather Forcast API System',
    'version': '0.0.1',
    'uiversion': 3,
    'openapi': '3.0.2',
}

swagger = Swagger(app)


@app.before_request
def create_session():
    flask.g.session = Session()
    flask.g.table_list = TableList() 

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    flask.g.session.commit()
    flask.g.session.close()

api.add_resource(Example, '/example')
api.add_resource(DateWeather, '/date_weather')
