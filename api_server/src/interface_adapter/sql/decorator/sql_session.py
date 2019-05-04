# coding=utf-8
"""
SQL session decorator.
"""
import traceback
from connexion import NoContent
from functools import wraps

from src.constants import CTX_SQL_SESSION, CTX_TESTING
from src.interface_adapter.sql.model.database import Database as Db
from src.util.context import build_context, log_extra
from src.util.log import LOG


def require_sql(f):
    """
    Populate the g.session with a SQLAlchemy session. The wrapper will also take care of the lifecycle of the session.
    If the function wrapped return something that is not a 2XX error code, the session will be automatically rollbacked.
    Otherwise it will commit.
    """

    @wraps(f)
    def wrapper(ctx, *args, **kwds):
        """
        Wrap http_api function.
        """
        # TODO: Remove dep from SQLAlchemy?
        if ctx.get(CTX_SQL_SESSION):
            return f(ctx, *args, **kwds)

        s = Db.get_db().get_session()
        ctx = build_context(session=s, ctx=ctx)

        try:
            result = f(ctx, *args, **kwds)

            # It makes things clearer and less error-prone.
            assert isinstance(result, tuple), "Please always pass the result AND the HTTP code."
            assert len(result) > 1, "Please always pass the result AND the HTTP code."

            status_code = result[1]
            msg = result[0]
            if result[0] == NoContent:
                msg = None
            if status_code and 200 <= status_code <= 299:
                s.commit()
            else:
                LOG.info("rollback_sql_transaction_non_200_http_code",
                         extra=log_extra(ctx, code=status_code, message=msg))
                s.rollback()
            return result

        except Exception as e:
            LOG.error("rollback_sql_transaction_exception_caught",
                      extra=log_extra(ctx, exception=str(e), traceback=traceback.format_exc()))
            s.rollback()
            raise

        finally:
            # When running unit tests, we don't close the session so tests can actually perform some work on that
            # session.
            if not ctx.get(CTX_TESTING):
                s.close()

    return wrapper
