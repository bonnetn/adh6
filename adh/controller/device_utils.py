from adh.model.models import Adherent, Portable, Ordinateur
from sqlalchemy.sql.expression import literal
from sqlalchemy.types import String


def is_wired(macAddress, s):
    """ Return true if the mac address corresponds to a wired device """
    queryWired = s.query(Ordinateur)
    queryWired = queryWired.filter(Ordinateur.mac == macAddress)

    return s.query(queryWired.exists()).scalar()


def is_wireless(macAddress, s):
    """ Return true if the mac address corresponds to a wireless device """
    queryWireless = s.query(Portable)
    queryWireless = queryWireless.filter(Portable.mac == macAddress)

    return s.query(queryWireless.exists()).scalar()


def create_wireless_device(body, s):
    """ Create a wireless device in the database """
    dev = Portable(
        mac=body['mac'],
        adherent=Adherent.find(s, body['username']),
    )
    s.add(dev)
    s.commit()


def create_wired_device(body, s):
    """ Create a wired device in the database """
    dev = Ordinateur(
        mac=body['mac'],
        ip=body['ipAddress'],
        ipv6=body['ipv6Address'],
        adherent=Adherent.find(s, body['username']),
    )
    s.add(dev)
    s.commit()


def update_wireless_device(macAddress, body, s):
    """ Update a wireless device in the database """
    q = s.query(Portable).filter(Portable.mac == macAddress)
    dev = q.one()
    dev.mac = body['mac']
    dev.adherent = Adherent.find(s, body['username'])
    s.commit()


def update_wired_device(macAddress, body, s):
    """ Update a wired device in the database """
    q = s.query(Ordinateur).filter(Ordinateur.mac == macAddress)
    dev = q.one()

    dev.mac = body['mac']
    dev.ip = body['ipAddress']
    dev.ipv6 = body['ipv6Address']
    dev.adherent = Adherent.find(s, body['username'])
    s.commit()


def delete_wireless_device(macAddress, s):
    """ Delete a wireless device from the database """
    q = s.query(Portable).filter(Portable.mac == macAddress)
    dev = q.one()
    s.delete(dev)
    s.commit()


def delete_wired_device(macAddress, s):
    """ Delete a wired device from the databse """
    q = s.query(Ordinateur).filter(Ordinateur.mac == macAddress)
    dev = q.one()
    s.delete(dev)
    s.commit()


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
