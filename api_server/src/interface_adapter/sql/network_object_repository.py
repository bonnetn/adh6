# coding=utf-8
"""
Implements everything related to actions on the SQL database.
This deals with all the network objects (except the member's devices).
"""
from datetime import datetime
from sqlalchemy import or_
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.port import Port, SwitchInfo
from src.entity.switch import Switch
from src.entity.vlan import Vlan
from src.exceptions import SwitchNotFoundError, PortNotFoundError, VLANNotFoundError, RoomNotFoundError
from src.interface_adapter.sql.model.models import Chambre
from src.interface_adapter.sql.model.models import Port as PortSQL
from src.interface_adapter.sql.model.models import Switch as SwitchSQL
from src.interface_adapter.sql.model.models import Vlan as VlanSQL
from src.use_case.interface.port_repository import PortRepository
from src.use_case.interface.switch_repository import SwitchRepository
from src.use_case.interface.vlan_repository import VLANRepository
from src.util.context import log_extra
from src.util.log import LOG


class NetworkObjectSQLRepository(PortRepository, VLANRepository, SwitchRepository):

    def search_switches_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, switch_id: str = None,
                           terms: str = None) -> (
            List[Switch], int):
        """
        Search for a switch.
        """
        LOG.debug("sql_network_object_repository_search_switch_by",
                  extra=log_extra(ctx, switch_id=switch_id, terms=terms))

        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SwitchSQL)

        if switch_id is not None:
            q = q.filter(SwitchSQL.id == switch_id)

        if terms is not None:
            q = q.filter(or_(
                SwitchSQL.description.contains(terms),
                SwitchSQL.ip.contains(terms),
            ))

        count = q.count()
        q = q.order_by(SwitchSQL.description.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        result = q.all()

        result = map(_map_switch_sql_to_entity, result)
        result = list(result)
        return result, count

    def create_switch(self, ctx, ip_v4=None, description=None, community=None) -> str:
        # Please do not log community...
        LOG.debug("sql_network_object_repository_create_switch",
                  extra=log_extra(ctx, ip_v4=ip_v4, description=description))

        s = ctx.get(CTX_SQL_SESSION)
        switch = SwitchSQL(
            ip=ip_v4,
            description=description,
            communaute=community,
        )
        s.add(switch)
        s.flush()

        return str(switch.id)

    def update_switch(self, ctx, switch_id, ip_v4=None, description=None, community=None) -> None:
        # Please do not log community...
        LOG.debug("sql_network_object_repository_update_switch",
                  extra=log_extra(ctx, switch_id=switch_id, ip_v4=ip_v4, description=description))

        s = ctx.get(CTX_SQL_SESSION)
        result: SwitchSQL = s.query(SwitchSQL).filter(SwitchSQL.id == int(switch_id)).one_or_none()
        if not result:
            raise SwitchNotFoundError(switch_id)

        result.communaute = community
        result.ip = ip_v4
        result.description = description

    def delete_switch(self, ctx, switch_id: str) -> None:
        LOG.debug("sql_network_object_repository_delete_switch", extra=log_extra(ctx, switch_id=switch_id))

        s = ctx.get(CTX_SQL_SESSION)
        result: SwitchSQL = s.query(SwitchSQL).filter(SwitchSQL.id == int(switch_id)).one_or_none()
        if not result:
            raise SwitchNotFoundError(switch_id)

        s.delete(result)

    def search_port_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, port_id: str = None,
                       switch_id: str = None,
                       room_number: str = None, terms: str = None) -> (List[Port], int):
        """
        Search for a port.
        :return: the ports and the number of matches in the DB.
        """
        LOG.debug("sql_network_object_repository_search_port_by",
                  extra=log_extra(ctx, port_id=port_id, switch_id=switch_id, room_number=room_number, terms=terms))

        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(PortSQL)

        if port_id:
            q = q.filter(PortSQL.id == port_id)

        if switch_id:
            q = q.join(SwitchSQL)
            q = q.filter(SwitchSQL.id == switch_id)

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
        """
        Create a port in the database
        :return the newly created port ID

        :raise InvalidRoomNumber
        :raise InvalidSwitchID
        """
        LOG.debug("sql_network_object_repository_create_port",
                  extra=log_extra(ctx, rcom=rcom, port_number=port_number, oid=oid, switch_id=switch_id,
                                  room_number=room_number))

        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        room = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
        if room is None:
            raise RoomNotFoundError(room_number)

        switch = s.query(SwitchSQL).filter(SwitchSQL.id == switch_id).one_or_none()
        if switch is None:
            raise SwitchNotFoundError(switch_id)

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

    def update_port(self, ctx, port_id=None, rcom=None, port_number=None, oid=None, switch_id=None,
                    room_number=None) -> None:
        """
        Update a port in the database
        :return the newly created port ID

        :raise PortNotFound
        :raise InvalidRoomNumber
        :raise InvalidSwitchID
        """
        LOG.debug("sql_network_object_repository_udpate_port",
                  extra=log_extra(ctx, port_id=port_id, rcom=rcom, port_number=port_number, oid=oid,
                                  switch_id=switch_id, room_number=room_number))

        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        port = s.query(PortSQL).filter(PortSQL.id == int(port_id)).one_or_none()
        if port is None:
            raise PortNotFoundError(port_id)

        room = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
        if room is None:
            raise RoomNotFoundError(room_number)

        switch = s.query(SwitchSQL).filter(SwitchSQL.id == switch_id).one_or_none()
        if switch is None:
            raise SwitchNotFoundError(switch_id)

        port.rcom = rcom
        port.numero = port_number
        port.oid = oid
        port.switch = switch
        port.chambre = room
        port.updated_at = now

    def delete_port(self, ctx, port_id: str) -> None:
        """
        Delete port

        :raise PortNotFound
        """
        s = ctx.get(CTX_SQL_SESSION)
        port = s.query(PortSQL).filter(PortSQL.id == port_id).one_or_none()
        if port is None:
            raise PortNotFoundError(port_id)

        s.delete(port)

    def get_vlan(self, ctx, vlan_number) -> Vlan:
        """
        Get a VLAN.

        :raise VlanNotFound
        """
        LOG.debug("sql_network_object_repository_get_vlan", extra=log_extra(ctx, vlan_number=vlan_number))

        s = ctx.get(CTX_SQL_SESSION)
        result = s.query(VlanSQL).filter(VlanSQL.numero == vlan_number).one_or_none()
        if not result:
            raise VLANNotFoundError(vlan_number)

        return _map_vlan_sql_to_entity(result)


def _map_vlan_sql_to_entity(r: VlanSQL) -> Vlan:
    return Vlan(
        number=str(r.numero),
        ip_v4_range=r.adresses,
        ip_v6_range=r.adressesv6,
    )


def _map_switch_sql_to_entity(r: SwitchSQL) -> Switch:
    return Switch(
        id=str(r.id),
        description=r.description,
        ip_v4=r.ip,
        community=r.communaute,
    )


def _map_port_sql_to_entity(r: PortSQL) -> Port:
    return Port(
        id=str(r.id),
        port_number=r.numero,
        room_number="aucun" if not r.chambre.numero else str(r.chambre.numero),
        switch_info=SwitchInfo(
            switch_id=str(r.switch.id),
            rcom=r.rcom,
            oid=r.oid,
        ),
    )
