from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

Base = declarative_base()


class Database():

    def __init__(self, db_settings, testing=False):
        self.engine = create_engine(URL(**db_settings), pool_recycle=3600)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        self.testing = testing

        self.db_session().begin_nested()

    def get_session(self):
        return self.db_session()

    def remove_session(self):
        return self.db_session.remove()

    def init_db(settings):
        Database.db = Database(settings)

    def get_db():
        return Database.db
