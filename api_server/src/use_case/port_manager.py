# coding=utf-8
from typing import List

from src.entity.port import Port
from src.log import LOG
from src.use_case.exceptions import IntMustBePositiveException
from src.use_case.interface.port_repository import PortRepository
from src.util.context import log_extra


class PortManager:
    def __init__(self, port_storage: PortRepository):
        self.port_storage = port_storage

    def search(self, ctx, limit=100, offset=0, switch_id=None, room_number=None, terms=None) -> (List[Port], int):
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.port_storage.search_port_by(ctx, limit=limit, offset=offset, switch_id=switch_id,
                                                         room_number=room_number, terms=terms)
        LOG.info("port_search", extra=log_extra(ctx, switch_id=switch_id, room_number=room_number, terms=terms))

        return result, count
