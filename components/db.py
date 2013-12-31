from __future__ import print_function

from pyaib.components import component_class
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@component_class("db")
class Database(object):
    def __init__(self, ctx, config):
        self.engine = create_engine(config["url"])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
