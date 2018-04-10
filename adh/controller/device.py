from connexion import NoContent
from adh.model.database import Database as db
from adh.model import models
import sqlalchemy
from adh.exceptions.invalid_email import InvalidEmail
from adh.exceptions.invalid_ip import InvalidIPv4, InvalidIPv6


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


def get_adherent(username):
    """ Return the adherent associated with the given username """
    s = db.get_db().get_session()
    q = s.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)
    return q.one()


def create_wireless_device(body):
    """ Create a wireless device in the database """
    s = db.get_db().get_session()
    dev = models.Portable(
        mac=body['mac'],
        adherent=get_adherent(body['username']),
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
        adherent=get_adherent(body['username']),
    )
    s.add(dev)
    s.commit()


def update_wireless_device(macAddress, body):
    """ Update a wireless device in the database """
    s = db.get_db().get_session()
    q = s.query(models.Portable).filter(models.Portable.mac == macAddress)
    dev = q.one()
    dev.mac = body['mac']
    dev.adherent = get_adherent(body['username'])
    s.commit()


def update_wired_device(macAddress, body):
    """ Update a wired device in the database """
    s = db.get_db().get_session()
    q = s.query(models.Ordinateur).filter(models.Ordinateur.mac == macAddress)
    dev = q.one()

    dev.mac = body['mac']
    dev.ip = body['ipAddress']
    dev.ipv6 = body['ipv6Address']
    dev.adherent = get_adherent(body['username'])
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


def filterDevice(limit=100, username=None, terms=None):
    """ [API] Filter the list of the devices according to some criterias """
    if limit < 0:
        return 'Limit must be a positive number', 400
    s = db.get_db().get_session()
    results = []

    if username:
        try:
            target = get_adherent(username)
        except sqlalchemy.orm.exc.NoResultFound:
            return [], 200

    q = s.query(models.Portable)
    if username:
        q = q.filter(models.Portable.adherent == target)
    if terms:
        q = q.filter(
            (models.Portable.mac.contains(terms)) |
            False  # TODO: compare on username ?
        )
    r = q.all()
    results += list(map(dict, r))

    q = s.query(models.Ordinateur)
    if username:
        q = q.filter(models.Ordinateur.adherent == target)
    if terms:
        q = q.filter(
            (models.Ordinateur.mac.contains(terms)) |
            (models.Ordinateur.ip.contains(terms)) |
            (models.Ordinateur.ipv6.contains(terms))
            # TODO: compare on username ?
        )
    r = q.all()
    results += list(map(dict, r))
    results = results[:limit]

    return results, 200


def putDevice(macAddress, body):
    """ [API] Put (update or create) a new device in the database """
    try:
        wired = is_wired(macAddress)
        wireless = is_wireless(macAddress)
        wanted_type = body["connectionType"]

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

    except sqlalchemy.orm.exc.NoResultFound:
        return 'Invalid username', 400

    except InvalidEmail:
        return 'Invalid email', 400

    except InvalidIPv6:
        return 'Invalid IPv6', 400

    except InvalidIPv4:
        return 'Invalid IPv4', 400


def getDevice(macAddress):
    """ [API] Return the device specified by the macAddress """
    s = db.get_db().get_session()
    if is_wireless(macAddress):
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == macAddress)
        r = q.one()
        return dict(r), 200
    elif is_wired(macAddress):
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == macAddress)
        r = q.one()
        return dict(r), 200
    else:
        return NoContent, 404


def deleteDevice(macAddress):
    """ [API] Delete the specified device from the database """
    s = db.get_db().get_session()
    if is_wireless(macAddress):
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == macAddress)
        r = q.one()
        s.delete(r)
        s.commit()
        return NoContent, 204

    elif is_wired(macAddress):
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == macAddress)
        r = q.one()
        s.delete(r)
        s.commit()
        return NoContent, 204

    else:
        return NoContent, 404
