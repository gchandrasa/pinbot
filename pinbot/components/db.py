from pyaib.components import component_class
from pyaib.plugins import observe
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


@observe("IRC_ONCONNECT")
def register_models(ctx):
    """Registers all classes that inherit base ``Model`` class.
    """
    Model.metadata.create_all(ctx.db.engine)
