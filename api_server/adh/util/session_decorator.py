from flask import g

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
            s.close()
            g.session = None

    return wrapper
