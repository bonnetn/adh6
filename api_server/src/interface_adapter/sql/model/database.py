import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.interface_adapter.sql.model.models import Base, NainA
from src.log import LOG


class Database():
    RETRY_COUNT = 10
    RETRY_INTERVAL = 10

    def __init__(self, db_settings, testing=False):
        self.testing = testing

        self.engine = create_engine(
            URL(**db_settings),
            isolation_level="SERIALIZABLE",  # As we don't have a lot of IO, we can afford the highest isolation.
            echo=False,  # Echo the SQL queries if testing. NOTE: removed, this breaks the tests
            pool_pre_ping=True,  # Make sure the connection is OK before using it.
        )

        self.session_maker = sessionmaker(
            bind=self.engine,
            autoflush=True,  # Flush at each query so that we can see our changes in the current session.
            autocommit=False,  # Never auto-commit, we want proper transactions!
        )

        if testing:
            self.session_maker = scoped_session(self.session_maker)

            # If testing, drop all tables & recreate them
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)

        else:
            # Create NainA table if not exists. (The other tables should already exist.)
            for retries in range(Database.RETRY_COUNT):
                try:
                    logging.info("connecting_to_database")
                    Base.metadata.create_all(
                        self.engine,
                        tables=[NainA.__table__]
                    )
                    logging.info("connection_established")
                    logging.info("table_created")
                except OperationalError as e:
                    LOG.warn("could_not_connect_to_database")
                    if retries + 1 == Database.RETRY_COUNT:
                        raise
                    time.sleep(Database.RETRY_INTERVAL)

    def get_session(self):
        return self.session_maker()

    db = None

    @staticmethod
    def init_db(settings, testing=False):
        Database.db = Database(settings, testing=testing)

    @staticmethod
    def get_db():
        if Database.db is None:
            raise AttributeError("database is none")
        return Database.db
