from connexion import NoContent
import datetime
import json
from adh.exceptions import UserNotFound
from adh.model.database import Database as db
from adh.model import models
from adh.model.models import Adherent
from sqlalchemy.orm.exc import MultipleResultsFound
from adh.exceptions import InvalidIPv4, InvalidIPv6, InvalidMac
from adh import ip_controller
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
import logging


@auth_simple_user
def filterDevice(admin, limit=100, offset=0, username=None, terms=None):
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
    logging.info("%s fetched the device list", admin.login)
    return results, 200, headers


def allocate_ip_for_device(s, dev):
    if dev.adherent.date_de_depart < datetime.datetime.now().date():
        dev.ip = "En Attente"
        dev.ipv6 = "En Attente"
        return  # No need to allocate ip for someone who is not a member

    if dev.ip == "En Attente":
        network = dev.adherent.chambre.vlan.adresses

        ip_controller.free_expired_devices(s)
        next_ip = ip_controller.get_available_ip(
                    network,
                    ip_controller.get_all_used_ipv4(s)
        )

        dev.ip = next_ip


@auth_simple_user
def putDevice(admin, macAddress, body):
    """ [API] Put (update or create) a new device in the database """
    s = db.get_db().get_session()
    try:
        wired = is_wired(macAddress, s)
        wireless = is_wireless(macAddress, s)
        wanted_type = body["connectionType"]

        returnCode = None

        if wired and wireless:
            if wanted_type == "wired":
                delete_wireless_device(admin, macAddress, s)
                device = update_wired_device(admin, macAddress, body, s)
                allocate_ip_for_device(s, device)
            else:
                delete_wired_device(admin, macAddress, s)
                update_wireless_device(admin, macAddress, body, s)
            returnCode = 204

        elif wired:
            if wanted_type == "wireless":
                delete_wired_device(admin, macAddress, s)
                create_wireless_device(admin, body, s)
            else:
                device = update_wired_device(admin, macAddress, body, s)
                allocate_ip_for_device(s, device)
            returnCode = 204

        elif wireless:
            if wanted_type == "wired":
                delete_wireless_device(admin, macAddress, s)
                device = create_wired_device(admin, body, s)
                allocate_ip_for_device(s, device)
            else:
                update_wireless_device(admin, macAddress, body, s)
            returnCode = 204

        else:  # Create device
            if body["mac"] != macAddress:
                return 'The MAC address in the query ' + \
                       'and in the body don\'t match', 400

            if wanted_type == "wired":
                device = create_wired_device(admin, body, s)
                allocate_ip_for_device(s, device)
            else:
                create_wireless_device(admin, body, s)
            returnCode = 201

        if returnCode == 204:
            logging.info("%s updated the device %s\n%s",
                         admin.login, macAddress, json.dumps(body,
                                                             sort_keys=True))

        elif returnCode == 201:
            logging.info("%s created the device %s\n%s",
                         admin.login, macAddress, json.dumps(body,
                                                             sort_keys=True))

        s.commit()
        return NoContent, returnCode

    except ip_controller.NoMoreIPAvailable:
        s.rollback()
        return 'No more ip available', 400

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
def getDevice(admin, macAddress):
    """ [API] Return the device specified by the macAddress """
    s = db.get_db().get_session()
    if is_wireless(macAddress, s):
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == macAddress)
        r = q.one()
        logging.info("%s fetched the device %s", admin.login, macAddress)
        return dict(r), 200

    elif is_wired(macAddress, s):
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == macAddress)
        r = q.one()
        logging.info("%s fetched the device %s", admin.login, macAddress)
        return dict(r), 200

    else:
        return NoContent, 404


@auth_simple_user
def deleteDevice(admin, macAddress):
    """ [API] Delete the specified device from the database """
    s = db.get_db().get_session()
    if is_wireless(macAddress, s):
        delete_wireless_device(admin, macAddress, s)
        logging.info("%s deleted the device %s", admin.login, macAddress)
        return NoContent, 204

    elif is_wired(macAddress, s):
        delete_wired_device(admin, macAddress, s)
        logging.info("%s deleted the device %s", admin.login, macAddress)
        return NoContent, 204

    else:
        return NoContent, 404
