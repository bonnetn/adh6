from connexion import NoContent

from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.health_manager import HealthManager
from src.util.context import log_extra
from src.util.log import LOG


class HealthHandler:
    def __init__(self, health_manager: HealthManager):
        self.health_manager = health_manager

    @with_context
    @require_sql
    def health(self, ctx):
        LOG.debug("http_health_called", extra=log_extra(ctx))

        if self.health_manager.is_healthy(ctx):
            return "OK", 200
        else:
            return "FAILURE", 503
