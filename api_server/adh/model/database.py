from flask import current_app
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database():

    def __init__(self, db_settings, testing=False):
        self.engine = create_engine(URL(**db_settings), pool_recycle=3600)

        @event.listens_for(self.engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            dbapi_connection.isolation_level = None

        @event.listens_for(self.engine, "begin")
        def do_begin(conn):
            # emit our own BEGIN
            conn.execute("BEGIN")

        self.session_maker = sessionmaker(bind=self.engine)
        if testing:
            self.session_maker = scoped_session(self.session_maker)
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.testing = testing

        self.session_maker().begin_nested()

    def get_session(self):
        return self.session_maker()

    db = None

    def init_db(settings, testing=False):
        Database.db = Database(settings, testing=testing)

    def get_db():
        return Database.db
