from src.use_case.interface.ping_repository import PingRepository
from src.util.context import log_extra
from src.util.log import LOG


class HealthManager:
    """
    Response to health requests.
    """

    def __init__(self, repository: PingRepository):
        self.health_repository = repository

    def is_healthy(self, ctx) -> bool:
        db_health = self.health_repository.ping(ctx)
        if not db_health:
            LOG.error("health_check_db_not_healthy", extra=log_extra(ctx))
            return False

        # TODO: add more health checks?

        LOG.info("health_check_success", extra=log_extra(ctx))
        return True
