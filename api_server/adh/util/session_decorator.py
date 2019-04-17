import logging

from flask import g, current_app

from adh.interface_adapter.sql.model.database import Database as Db


def require_sql(f):
    """
    Populate the g.session with a SQLAlchemy session. The wrapper will also take care of the lifecycle of the session.
    If the function wrapped return something that is not a 2XX error code, the session will be automatically rollbacked.
    Otherwise it will commit.
    """

    def wrapper(*args, **kwargs):
        if "session" in g:
            return f(*args, **kwargs)

        g.session = s = Db.get_db().get_session()
        try:
            result = f(*args, **kwargs)

            # It makes things clearer and less error-prone.
            assert isinstance(result, tuple), "Please always pass the result AND the HTTP code."
            assert len(result) > 1, "Please always pass the result AND the HTTP code."

            status_code = result[1]
            if status_code and 200 <= status_code <= 299:
                s.commit()
            else:
                logging.info("Status code %d not 2XX, rollbacking.", status_code)
                s.rollback()
            return result
        except Exception:
            logging.warn("Exception caught, rollbacking.")
            s.rollback()
            raise
        finally:
            # When running unit tests, we don't close the session so tests can actually perform some work on that
            # session.
            if not current_app.config["TESTING"]:
                s.close()
                g.session = None

    return wrapper
