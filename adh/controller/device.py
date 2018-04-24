from connexion import NoContent
from adh.exceptions import UserNotFound
from adh.model.database import Database as db
from adh.model import models
from adh.model.models import Adherent
from adh.exceptions import InvalidIPv4, InvalidIPv6, InvalidMac
from sqlalchemy.sql.expression import literal
from sqlalchemy.types import String


def query_all_devices(s):

    q_wired = s.query(
        models.Ordinateur.mac.label("mac"),
        models.Ordinateur.ip.label("ip"),
        models.Ordinateur.ipv6.label("ipv6"),
        models.Ordinateur.adherent_id.label("adherent_id"),
        literal("wired", type_=String).label("type"),
    )

    q_wireless = s.query(
        models.Portable.mac.label("mac"),
        literal(None, type_=String).label("ip"),
        literal(None, type_=String).label("ipv6"),
        models.Portable.adherent_id.label("adherent_id"),
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


def is_wired(macAddress):
    """ Return true if the mac address corresponds to a wired device """
    session = db.get_db().get_session()
    queryWired = session.query(models.Ordinateur)
    queryWired = queryWired.filter(models.Ordinateur.mac == macAddress)

    return session.query(queryWired.exists()).scalar()


def is_wireless(macAddress):
    """ Return true if the mac address corresponds to a wireless device """
    session = db.get_db().get_session()
    queryWireless = session.query(models.Portable)
    queryWireless = queryWireless.filter(models.Portable.mac == macAddress)

    return session.query(queryWireless.exists()).scalar()


def create_wireless_device(body):
    """ Create a wireless device in the database """
    s = db.get_db().get_session()
    dev = models.Portable(
        mac=body['mac'],
        adherent=Adherent.find(s, body['username']),
    )
    s.add(dev)
    s.commit()


def create_wired_device(body):
    """ Create a wired device in the database """
    s = db.get_db().get_session()
    dev = models.Ordinateur(
        mac=body['mac'],
        ip=body['ipAddress'],
        ipv6=body['ipv6Address'],
        adherent=Adherent.find(s, body['username']),
    )
    s.add(dev)
    s.commit()


def update_wireless_device(macAddress, body):
    """ Update a wireless device in the database """
    s = db.get_db().get_session()
    q = s.query(models.Portable).filter(models.Portable.mac == macAddress)
    dev = q.one()
    dev.mac = body['mac']
    dev.adherent = Adherent.find(s, body['username'])
    s.commit()


def update_wired_device(macAddress, body):
    """ Update a wired device in the database """
    s = db.get_db().get_session()
    q = s.query(models.Ordinateur).filter(models.Ordinateur.mac == macAddress)
    dev = q.one()

    dev.mac = body['mac']
    dev.ip = body['ipAddress']
    dev.ipv6 = body['ipv6Address']
    dev.adherent = Adherent.find(s, body['username'])
    s.commit()


def delete_wireless_device(macAddress):
    """ Delete a wireless device from the database """
    s = db.get_db().get_session()
    q = s.query(models.Portable).filter(models.Portable.mac == macAddress)
    dev = q.one()
    s.delete(dev)
    s.commit()


def delete_wired_device(macAddress):
    """ Delete a wired device from the databse """
    s = db.get_db().get_session()
    q = s.query(models.Ordinateur).filter(models.Ordinateur.mac == macAddress)
    dev = q.one()
    s.delete(dev)
    s.commit()


def filterDevice(limit=100, offset=0, username=None, terms=None):
    """ [API] Filter the list of the devices according to some criterias """
    if limit < 0:
        return 'Limit must be a positive number', 400
    s = db.get_db().get_session()

    if username:
        try:
            target = Adherent.find(s, username)
        except UserNotFound:
            return [], 200

    all_devices = query_all_devices(s)

    q = s.query(all_devices, Adherent.login.label("login"))
    q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)
    if username:
        q = q.filter(Adherent.login == target.login)
    if terms:
        q = q.filter(
            (all_devices.columns.mac.contains(terms)) |
            (all_devices.columns.ip.contains(terms)) |
            (all_devices.columns.ipv6.contains(terms)) |
            (Adherent.login.contains(terms))
        )

    q = q.offset(offset)
    q = q.limit(limit)
    r = q.all()
    results = list(map(dev_to_dict, r))

    return results, 200


def putDevice(macAddress, body):
    """ [API] Put (update or create) a new device in the database """
    try:
        wired = is_wired(macAddress)
        wireless = is_wireless(macAddress)
        wanted_type = body["connectionType"]

        # TODO: Make proper IP assignement system
        if wanted_type == "wired":
            if 'ipAddress' not in body:
                body['ipAddress'] = '192.168.0.1'
            if 'ipv6Address' not in body:
                body['ipv6Address'] = 'fe80::1'

        if wired and wireless:
            if wanted_type == "wired":
                delete_wireless_device(macAddress)
                update_wired_device(macAddress, body)
            else:
                delete_wired_device(macAddress)
                update_wireless_device(macAddress, body)
        elif wired:
            if wanted_type == "wireless":
                delete_wired_device(macAddress)
                create_wireless_device(body)
            else:
                update_wired_device(macAddress, body)
        elif wireless:
            if wanted_type == "wired":
                delete_wireless_device(macAddress)
                create_wired_device(body)
            else:
                update_wireless_device(macAddress, body)
        else:  # Create device
            if body["mac"] != macAddress:
                return 'The MAC address in the query ' + \
                       'and in the body don\'t match', 400

            if wanted_type == "wired":
                create_wired_device(body)
            else:
                create_wireless_device(body)
            return NoContent, 201
        return NoContent, 204

    except UserNotFound:
        return 'User not found', 400

    except InvalidMac:
        return 'Invalid mac', 400

    except InvalidIPv6:
        return 'Invalid IPv6', 400

    except InvalidIPv4:
        return 'Invalid IPv4', 400


def getDevice(macAddress):
    """ [API] Return the device specified by the macAddress """
    if is_wireless(macAddress):
        s = db.get_db().get_session()
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == macAddress)
        r = q.one()
        return dict(r), 200

    elif is_wired(macAddress):
        s = db.get_db().get_session()
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == macAddress)
        r = q.one()
        return dict(r), 200

    else:
        return NoContent, 404


def deleteDevice(macAddress):
    """ [API] Delete the specified device from the database """
    if is_wireless(macAddress):
        delete_wireless_device(macAddress)
        return NoContent, 204

    elif is_wired(macAddress):
        delete_wired_device(macAddress)
        return NoContent, 204

    else:
        return NoContent, 404
