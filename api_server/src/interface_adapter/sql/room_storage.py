# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from datetime import datetime
from sqlalchemy import or_
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.room import Room
from src.interface_adapter.sql.model.models import Adherent, Chambre, Vlan
from src.use_case.interface.member_repository import NotFoundError
from src.use_case.interface.room_repository import RoomRepository
from src.use_case.util.exceptions import RoomAlreadyExists, InvalidVLANNumberError
from src.util.context import log_extra
from src.util.log import LOG


class RoomSQLStorage(RoomRepository):
    def search_room_by(self, ctx, limit=100, offset=0, room_number=None, owner_username=None, terms=None) -> (
            List[Room], int):
        LOG.debug("sql_room_storage_search_room_by_called", extra=log_extra(ctx, username=owner_username, terms=terms))
        s = ctx.get(CTX_SQL_SESSION)
        q = s.query(Chambre)

        if room_number:
            q = q.filter(Chambre.numero == room_number)

        if terms:
            q = q.filter(or_(
                Chambre.telephone.contains(terms),
                Chambre.description.contains(terms),
            ))

        if owner_username:
            q = q.join(Adherent)
            q = q.filter(Adherent.login == owner_username)

        count = q.count()
        q = q.order_by(Chambre.numero.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()
        r = list(map(_map_room_sql_to_entity, r))
        return r, count

    def update_room(self, ctx, room_to_update, room_number=None, description=None, phone_number=None,
                    vlan_number=None) -> None:
        LOG.debug("sql_room_storage_update_room_called",
                  extra=log_extra(ctx, room_number=room_number, description=description, phone_number=phone_number,
                                  vlan_number=vlan_number))
        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        room = s.query(Chambre).filter(Chambre.numero == room_to_update).one_or_none()
        if room is None:
            raise NotFoundError()

        vlan = s.query(Vlan).filter(Vlan.numero == vlan_number).one_or_none()
        if vlan is None:
            raise InvalidVLANNumberError()

        room.numero = int(room_number)
        room.description = description
        room.telephone = phone_number
        room.updated_at = now
        room.vlan = vlan

    def create_room(self, ctx, room_number=None, description=None, phone_number=None, vlan_number=None) -> None:
        LOG.debug("sql_room_storage_create_room_called",
                  extra=log_extra(ctx, room_number=room_number, description=description, phone_number=phone_number,
                                  vlan_number=vlan_number))
        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        result = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
        if result is not None:
            raise RoomAlreadyExists()

        vlan = s.query(Vlan).filter(Vlan.numero == vlan_number).one_or_none()
        if vlan is None:
            raise InvalidVLANNumberError()

        room = Chambre(
            numero=int(room_number),
            description=description,
            telephone=phone_number,
            created_at=now,
            updated_at=now,
            vlan=vlan,
        )

        s.add(room)

    def delete_room(self, ctx, room_number) -> None:
        LOG.debug("sql_room_storage_delete_room_called", extra=log_extra(ctx, room_number=room_number))
        s = ctx.get(CTX_SQL_SESSION)

        room = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
        if room is None:
            raise NotFoundError()

        s.delete(room)


def _map_room_sql_to_entity(r: Chambre) -> Room:
    vlan_number = None
    if r.vlan is not None:
        vlan_number = str(r.vlan.numero)

    return Room(
        room_number=str(r.numero),
        description=r.description,
        phone_number=r.telephone,
        vlan_number=vlan_number
    )
