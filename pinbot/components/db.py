from __future__ import print_function

from pyaib.components import component_class
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#: a base model that should be inherited by all submodels,
#: in order to be mapped into SQLAlchemy session automatically
Model = declarative_base()


@component_class("db")
class Database(object):
    def __init__(self, ctx, config):
        self.engine = create_engine(config["url"])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
