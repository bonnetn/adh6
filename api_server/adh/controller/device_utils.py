from sqlalchemy.sql.expression import literal
from sqlalchemy.types import String

from adh.model.models import Adherent, Portable, Ordinateur, Modification


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


def create_wireless_device(admin, body, s):
    """ Create a wireless device in the database """
    dev = Portable(
        mac=body['mac'],
        adherent=Adherent.find(s, body['username']),
    )

    s.add(dev)

    Modification.add_and_commit(s, dev, admin)
    return dev


def create_wired_device(admin, body, s):
    """ Create a wired device in the database """
    dev = Ordinateur(
        mac=body['mac'],
        ip=body.get('ipAddress', 'En Attente'),
        ipv6=body.get('ipv6Address', 'En Attente'),
        adherent=Adherent.find(s, body['username']),
    )

    s.add(dev)

    Modification.add_and_commit(s, dev, admin)
    return dev


def update_wireless_device(admin, mac_address, body, s):
    """ Update a wireless device in the database """
    q = s.query(Portable).filter(Portable.mac == mac_address)
    dev = q.one()

    dev.start_modif_tracking()
    dev.mac = body['mac']
    dev.adherent = Adherent.find(s, body['username'])

    Modification.add_and_commit(s, dev, admin)
    return dev


def update_wired_device(admin, mac_address, body, s):
    """ Update a wired device in the database """
    q = s.query(Ordinateur).filter(Ordinateur.mac == mac_address)
    dev = q.one()

    dev.start_modif_tracking()
    dev.mac = body['mac']
    dev.ip = body.get('ipAddress', 'En Attente')
    dev.ipv6 = body.get('ipv6Address', 'En Attente')
    dev.adherent = Adherent.find(s, body['username'])

    Modification.add_and_commit(s, dev, admin)
    return dev


def delete_wired_device(admin, mac_address, s):
    """ Delete a wired device from the databse """
    q = s.query(Ordinateur).filter(Ordinateur.mac == mac_address)
    dev = q.one()

    dev.start_modif_tracking()
    s.delete(dev)

    Modification.add_and_commit(s, dev, admin)


def delete_wireless_device(admin, mac_address, s):
    """ Delete a wireless device from the database """
    q = s.query(Portable).filter(Portable.mac == mac_address)
    dev = q.one()

    dev.start_modif_tracking()
    s.delete(dev)

    Modification.add_and_commit(s, dev, admin)


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
