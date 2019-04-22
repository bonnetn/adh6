# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from sqlalchemy import literal, String
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.device import Device, DeviceType
from src.interface_adapter.sql.model.models import Adherent, Ordinateur, Portable
from src.interface_adapter.sql.util.ip_controller import _get_available_ip, _get_all_used_ipv4, _get_all_used_ipv6
from src.use_case.interface.device_repository import DeviceRepository
from src.use_case.interface.ip_allocator import IPAllocator


class NoMoreIPAvailable(Exception):
    pass


class DeviceSQLStorage(DeviceRepository, IPAllocator):

    def search_device_by(self, ctx, limit=None, offset=None, mac_address=None, username=None, terms=None) \
            -> (List[Device], int):
        s = ctx.get(CTX_SQL_SESSION)

        # Return a subquery with all devices (wired & wireless)
        # The fields, ip, ipv6, dns, etc, are set to None for wireless devices
        # There is also a field "type" wich is wired and wireless
        all_devices = _get_all_devices(s)

        # Query all devices and their owner's unsername
        q = s.query(all_devices, Adherent.login.label("login"))
        q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)

        if mac_address:
            q = q.filter(all_devices.columns.mac == mac_address)

        if username:
            q = q.filter(Adherent.login == username)

        if terms:
            q = q.filter(
                (all_devices.columns.mac.contains(terms)) |
                (all_devices.columns.ip.contains(terms)) |
                (all_devices.columns.ipv6.contains(terms)) |
                (Adherent.login.contains(terms))
            )
        count = q.count()
        q = q.order_by(all_devices.columns.mac.asc())
        if offset is not None:
            q = q.offset(offset)
        if limit is not None:
            q = q.limit(limit)
        r = q.all()
        results = list(map(_map_device_sql_to_entity, r))

        return results, count

    def create_device(self, ctx, mac_address=None, owner_username=None, connection_type=None, ip_address=None,
                      ipv6_address=None):
        pass

    def allocate_ip_v4(self, ctx, ip_range: str) -> str:
        s = ctx.get(CTX_SQL_SESSION)
        return _get_available_ip(ip_range, _get_all_used_ipv4(s))

    def allocate_ip_v6(self, ctx, ip_range: str) -> str:
        s = ctx.get(CTX_SQL_SESSION)
        return _get_available_ip(ip_range, _get_all_used_ipv6(s))


def _map_device_sql_to_entity(d) -> Device:
    """
    Map a Device object from SQLAlchemy to a Device (from the entity folder/layer).
    """
    t = DeviceType.Wired
    if d.type == 'wireless':
        t = DeviceType.Wireless
    return Device(
        mac=d.mac,
        owner_username=d.login,
        connection_type=t,
        ip_address=d.ip,
        ipv6_address=d.ipv6,
    )


def _get_all_devices(s):
    q_wired = s.query(
        Ordinateur.mac.label("mac"),
        Ordinateur.ip.label("ip"),
        Ordinateur.ipv6.label("ipv6"),
        Ordinateur.adherent_id.label("adherent_id"),
        literal("wired", type_=String).label("type"),
    )

    q_wireless = s.query(
        Portable.mac.label("mac"),
        literal(None, type_=String).label("ip"),
        literal(None, type_=String).label("ipv6"),
        Portable.adherent_id.label("adherent_id"),
        literal("wireless", type_=String).label("type"),
    )
    q = q_wireless.union_all(q_wired)
    return q.subquery()
