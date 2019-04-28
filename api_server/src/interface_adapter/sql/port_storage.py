# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from sqlalchemy import or_
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.port import Port
from src.interface_adapter.sql.model.models import Chambre, Switch
from src.interface_adapter.sql.model.models import Port as PortSQL
from src.log import LOG
from src.use_case.interface.port_repository import PortRepository
from src.util.context import log_extra


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

        result = map(dict, result)
        result = list(result)
        return result, count
