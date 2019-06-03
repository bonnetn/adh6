from sqlalchemy.exc import SQLAlchemyError

from src.constants import CTX_SQL_SESSION
from src.use_case.interface.ping_repository import PingRepository
from src.util.context import log_extra
from src.util.log import LOG


class PingSQLRepository(PingRepository):
    def ping(self, ctx) -> bool:
        LOG.debug("sql_ping", extra=log_extra(ctx))

        s = ctx.get(CTX_SQL_SESSION)
        try:
            result = s.execute('SELECT 42').fetchall()
            if 1 != len(result):
                return False

            return [('42', 42)] == result[0].items()

        except SQLAlchemyError:
            return False
