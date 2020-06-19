#! /usr/bin/env python

from flask import Flask
from flasgger import Swagger
from flask_restful import Api, Resource
from resources import Example

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

api.add_resource(Example, '/example')
