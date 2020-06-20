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
from sqlalchemy import Table, MetaData, create_engine, and_, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.automap import automap_base

engine = create_engine("postgresql:///weather")
Base = automap_base()
Base.prepare(engine, reflect=True)
metadata = MetaData()
metadata.reflect(bind=engine)
Session = sessionmaker(bind=engine)

class TableList:
    def __init__(self):
        pass

    def get_table(self, table_name):
        return getattr(Base.classes, table_name)

    def __getitem__(self, table_name):
        return self.get_table(table_name)

    @property
    def names(self):
        return list(metadata.tables.keys())

if __name__ == "__main__":
    tl = TableList()
    print(tl.names)
    print(tl["weather_param"])
    import datetime
    wp_table = tl["weather_param"]
    cmd = Session().query(wp_table).filter(and_(wp_table.record_time > datetime.datetime.now() - datetime.timedelta(hours=2),
                                           wp_table.record_time < datetime.datetime.now() - datetime.timedelta(hours=1)))
    for rec in cmd.all():
        print(rec.temperature, rec.record_time)
