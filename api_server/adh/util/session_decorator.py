from flask import g, current_app

from adh.model.database import Database as Db


def require_sql(f):
    def wrapper(*args, **kwargs):
        if "session" in g:
            return f(*args, **kwargs)

        g.session = s = Db.get_db().get_session()
        try:
            result = f(*args, **kwargs)
            s.commit()
            return result
        except Exception:
            s.rollback()
            raise
        finally:
            # When running unit tests, we don't close the session so tests can actually perform some work on that
            # session.
            if not current_app.config["TESTING"]:
                s.close()
                g.session = None

    return wrapper
