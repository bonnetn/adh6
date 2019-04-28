# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from datetime import datetime
from sqlalchemy import or_
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.port import Port, SwitchInfo
from src.interface_adapter.sql.model.models import Chambre, Switch
from src.interface_adapter.sql.model.models import Port as PortSQL
from src.use_case.interface.port_repository import PortRepository, InvalidSwitchID, InvalidRoomNumber
from src.util.context import log_extra
from src.util.log import LOG


class PortSQLStorage(PortRepository):

    def search_port_by(self, ctx, limit=0, offset=0, port_id: str = None, switch_id: str = None,
                       room_number: str = None, terms: str = None) -> (List[Port], int):
        LOG.debug("sql_port_storage_search_port_by",
                  extra=log_extra(ctx, port_id=port_id, switch_id=switch_id, room_number=room_number, terms=terms))

        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(PortSQL)

        if port_id:
            q = q.filter(PortSQL.id == port_id)

        if switch_id:
            q = q.join(Switch)
            q = q.filter(Switch.id == switch_id)

        if room_number:
            q = q.join(Chambre)
            q = q.filter(Chambre.numero == room_number)

        if terms:
            q = q.filter(or_(
                PortSQL.numero.contains(terms),
                PortSQL.oid.contains(terms),
            ))

        count = q.count()
        q = q.order_by(PortSQL.switch_id.asc(), PortSQL.numero.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        result = q.all()

        result = map(_map_port_sql_to_entity, result)
        result = list(result)
        return result, count

    def create_port(self, ctx, rcom=None, port_number=None, oid=None, switch_id=None, room_number=None) -> str:
        """ [API] Create a port in the database """
        LOG.debug("sql_port_storage_create_port",
                  extra=log_extra(ctx, rcom=rcom, port_number=port_number, oid=oid, switch_id=switch_id,
                                  room_number=room_number))

        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        room = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
        if room is None:
            raise InvalidRoomNumber()

        switch = s.query(Switch).filter(Switch.id == switch_id).one_or_none()
        if switch is None:
            raise InvalidSwitchID()

        port = PortSQL(
            rcom=rcom,
            numero=port_number,
            oid=oid,
            switch=switch,
            chambre=room,
            created_at=now,
            updated_at=now,
        )
        s.add(port)
        s.flush()

        return str(port.id)


def _map_port_sql_to_entity(r: PortSQL) -> Port:
    return Port(
        id=str(r.id),
        port_number=r.numero,
        room_number=str(r.chambre.numero),
        switch_info=SwitchInfo(
            switch_id=str(r.switch.id),
            rcom=r.rcom,
            oid=r.oid,
        ),
    )
