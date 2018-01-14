from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings

Base = declarative_base()


class Database():

    def __init__(self, db_settings):
        self.engine = create_engine(URL(**db_settings), pool_recycle=3600)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        # Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.db_session()


# Connect to SQL database
db = Database(settings.DATABASE)
