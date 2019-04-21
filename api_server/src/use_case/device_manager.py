from typing import List

from src.entity.device import DeviceInfo
from src.log import LOG
from src.use_case.exceptions import IntMustBePositiveException
from src.use_case.interface.device_repository import DeviceRepository
from src.util.context import build_log_extra


class DeviceManager:
    def __init__(self,
                 device_storage: DeviceRepository):
        self.device_storage = device_storage

    def search(self, ctx, limit=100, offset=0, username=None, terms=None) -> (List[DeviceInfo], int):
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.device_storage.search_device_by(ctx, limit=limit, offset=offset, username=username,
                                                             terms=terms)

        LOG.info("device_search", extra=build_log_extra(
            ctx,
            limit=limit,
            terms=terms,
        ))

        return result, count
