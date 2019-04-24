# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.room import Room, Vlan
from src.interface_adapter.sql.model.models import Adherent, Chambre
from src.use_case.interface.room_repository import RoomRepository


class RoomSQLStorage(RoomRepository):

    def search_room_by(self, ctx, owner_username=None) -> (List[Room], int):
        s = ctx.get(CTX_SQL_SESSION)
        q = s.query(Chambre).join(Adherent)
        if owner_username:
            q = q.filter(Adherent.login == owner_username)

        count = q.count()
        q = q.order_by(Chambre.numero.asc())
        # if offset is not None:
        #     q = q.offset(offset)
        # if limit is not None:
        #     q = q.limit(limit)
        r = q.all()
        r = list(map(_map_room_sql_to_entity, r))
        return r, count


def _map_room_sql_to_entity(r: Chambre) -> Room:
    vlan = None
    if r.vlan is not None:
        vlan = Vlan(
            number=str(r.vlan.numero),
            ip_v4_range=r.vlan.adresses,
            ip_v6_range=r.vlan.adressesv6,
        )

    return Room(
        room_number=str(r.numero),
        description=r.description,
        phone_number=r.telephone,
        vlan=vlan,
    )
