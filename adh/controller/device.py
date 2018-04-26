from connexion import NoContent
from adh.exceptions import UserNotFound
from adh.model.database import Database as db
from adh.model import models
from adh.model.models import Adherent
from sqlalchemy.orm.exc import MultipleResultsFound
from adh.exceptions import InvalidIPv4, InvalidIPv6, InvalidMac
from adh.controller.device_utils import is_wired, is_wireless, \
        delete_wireless_device, \
        delete_wired_device, \
        update_wireless_device, \
        update_wired_device, \
        create_wireless_device, \
        create_wired_device, \
        get_all_devices, \
        dev_to_dict
from adh.auth import auth_simple_user


@auth_simple_user
def filterDevice(limit=100, offset=0, username=None, terms=None):
    """ [API] Filter the list of the devices according to some criterias """
    s = db.get_db().get_session()

    if limit < 0:
        return 'Limit must be a positive number', 400

    # Return a subquery with all devices (wired & wireless)
    # The fields, ip, ipv6, dns, etc, are set to None for wireless devices
    # There is also a field "type" wich is wired and wireless
    all_devices = get_all_devices(s)

    # Query all devices and their owner's unsername
    q = s.query(all_devices, Adherent.login.label("login"))
    q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)

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
    q = q.offset(offset)
    q = q.limit(limit)
    r = q.all()
    results = list(map(dev_to_dict, r))

    headers = {
        "X-Total-Count": count,
        "access-control-expose-headers": "X-Total-Count"
    }
    return results, 200, headers


@auth_simple_user
def putDevice(macAddress, body):
    """ [API] Put (update or create) a new device in the database """
    s = db.get_db().get_session()
    try:
        wired = is_wired(macAddress, s)
        wireless = is_wireless(macAddress, s)
        wanted_type = body["connectionType"]

        # TODO: Make proper IP assignement system
        if wanted_type == "wired":
            if 'ipAddress' not in body:
                body['ipAddress'] = '192.168.0.1'
            if 'ipv6Address' not in body:
                body['ipv6Address'] = 'fe80::1'

        if wired and wireless:
            if wanted_type == "wired":
                delete_wireless_device(macAddress, s)
                update_wired_device(macAddress, body, s)
            else:
                delete_wired_device(macAddress, s)
                update_wireless_device(macAddress, body, s)
        elif wired:
            if wanted_type == "wireless":
                delete_wired_device(macAddress, s)
                create_wireless_device(body, s)
            else:
                update_wired_device(macAddress, body, s)
        elif wireless:
            if wanted_type == "wired":
                delete_wireless_device(macAddress, s)
                create_wired_device(body, s)
            else:
                update_wireless_device(macAddress, body, s)
        else:  # Create device
            if body["mac"] != macAddress:
                return 'The MAC address in the query ' + \
                       'and in the body don\'t match', 400

            if wanted_type == "wired":
                create_wired_device(body, s)
            else:
                create_wireless_device(body, s)
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
    except MultipleResultsFound:
        return 'Multiple records for that MAC address found in database. ' + \
               'A MAC address should be unique. Fix your database.', 500


@auth_simple_user
def getDevice(macAddress):
    """ [API] Return the device specified by the macAddress """
    s = db.get_db().get_session()
    if is_wireless(macAddress, s):
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == macAddress)
        r = q.one()
        return dict(r), 200

    elif is_wired(macAddress, s):
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == macAddress)
        r = q.one()
        return dict(r), 200

    else:
        return NoContent, 404


@auth_simple_user
def deleteDevice(macAddress):
    """ [API] Delete the specified device from the database """
    s = db.get_db().get_session()
    if is_wireless(macAddress, s):
        delete_wireless_device(macAddress, s)
        return NoContent, 204

    elif is_wired(macAddress, s):
        delete_wired_device(macAddress, s)
        return NoContent, 204

    else:
        return NoContent, 404
