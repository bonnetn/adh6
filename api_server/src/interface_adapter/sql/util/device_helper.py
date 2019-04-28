from sqlalchemy.sql.expression import literal
from sqlalchemy.types import String

from src.interface_adapter.sql.model.models import Adherent, Portable, Ordinateur
from src.interface_adapter.sql.track_modifications import track_modifications


def is_wired(mac_address, s):
    """ Return true if the mac address corresponds to a wired device """
    query_wired = s.query(Ordinateur)
    query_wired = query_wired.filter(Ordinateur.mac == mac_address)

    return s.query(query_wired.exists()).scalar()


def is_wireless(mac_address, s):
    """ Return true if the mac address corresponds to a wireless device """
    query_wireless = s.query(Portable)
    query_wireless = query_wireless.filter(Portable.mac == mac_address)

    return s.query(query_wireless.exists()).scalar()


def create_wireless_device(ctx, mac_address, username, s):
    """ Create a wireless device in the database """
    dev = Portable(
        mac=mac_address,
        adherent=s.query(Adherent).filter(Adherent.login == username).one(),
    )

    with track_modifications(ctx, s, dev):
        s.add(dev)

    return dev


def create_wired_device(ctx, mac_address, ip_v4_address, ip_v6_address, username, s):
    """ Create a wired device in the database """
    dev = Ordinateur(
        mac=mac_address,
        ip=ip_v4_address,
        ipv6=ip_v6_address,
        adherent=s.query(Adherent).filter(Adherent.login == username).one(),
    )

    with track_modifications(ctx, s, dev):
        s.add(dev)

    return dev


def update_wireless_device(ctx, s, device_to_update, mac_address=None, username=None):
    """ Update a wireless device in the database """
    q = s.query(Portable).filter(Portable.mac == device_to_update)
    dev = q.one()

    with track_modifications(ctx, s, dev):
        dev.mac = mac_address or dev.mac
        if username:
            dev.adherent = s.query(Adherent).filter(Adherent.login == username).one()

    return dev


def update_wired_device(ctx, s, device_to_update, mac_address=None, username=None, ip_v4_address=None,
                        ip_v6_address=None):
    """ Update a wired device in the database """
    q = s.query(Ordinateur).filter(Ordinateur.mac == device_to_update)
    dev = q.one()

    with track_modifications(ctx, s, dev):
        dev.ip = ip_v4_address or dev.ip
        dev.ipv6 = ip_v6_address or dev.ipv6
        dev.mac = mac_address or dev.mac
        if username:
            dev.adherent = s.query(Adherent).filter(Adherent.login == username).one()

    return dev


def delete_wired_device(ctx, s, mac_address):
    """ Delete a wired device from the databse """
    q = s.query(Ordinateur).filter(Ordinateur.mac == mac_address)
    dev = q.one()

    with track_modifications(ctx, s, dev):
        s.delete(dev)


def delete_wireless_device(ctx, s, mac_address):
    """ Delete a wireless device from the database """
    q = s.query(Portable).filter(Portable.mac == mac_address)
    dev = q.one()

    with track_modifications(ctx, s, dev):
        s.delete(dev)


def get_all_devices(s):
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


def _dev_to_gen(d):
    yield "mac", d.mac,
    yield "connectionType", d.type,
    if d.ip:
        yield "ipAddress", d.ip
    if d.ipv6:
        yield "ipv6Address", d.ipv6
    yield "username", d.login


def dev_to_dict(d):
    return dict(_dev_to_gen(d))
