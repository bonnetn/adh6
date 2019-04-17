import logging

import sqlalchemy

from adh.constants import CTX_SQL_SESSION, CTX_ADMIN
from adh.exceptions import MustBePositiveException
from adh.interface_adapter.sql.model.models import Adherent, Chambre
from adh.use_case.interface.member_repository import MemberRepository
from adh.use_case.interface.room_repository import RoomRepository


class MemberManager:
    def __init__(self,
                 member_storage: MemberRepository):
        self.member_storage = member_storage

    def search(self, ctx, limit, offset=0, room_number=None, terms=None):

        if limit < 0:
            raise MustBePositiveException('limit')

        if offset < 0:
            raise MustBePositiveException('offset')

        result, count = self.member_storage.search_member_by(ctx,
                                                             limit=limit,
                                                             offset=offset,
                                                             room_number=room_number,
                                                             terms=terms)

        logging.info("%s fetched the member list", ctx.get(CTX_ADMIN))
        return result, count

