#! /usr/bin/env python

""" This script is used to manipulate postgresql database for flask server
    Authored by Victor Zhang, 06/12/2020
    This is the best practice recommended by:
    https://stackoverflow.com/questions/43459182/proper-sqlalchemy-use-in-flask
"""

import flask

import sqlalchemy
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert

from weather_restful import app

engine = create_engine("postgresql:///weather", echo=True)
Session = sessionmaker(bind=engine)

@app.before_request
def create_session():
    flask.g.session = Session()

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    flask.g.session.commit()
    flask.g.session.remove()


if __name__ == "__main__":
    pass
