import datetime
import json
import logging

from connexion import NoContent
from flask import g
from sqlalchemy.orm.exc import MultipleResultsFound

from adh import ip_controller
from adh.auth import auth_regular_admin
from adh.controller.device_utils import is_wired, is_wireless, \
    delete_wireless_device, \
    delete_wired_device, \
    update_wireless_device, \
    update_wired_device, \
    create_wireless_device, \
    create_wired_device, \
    get_all_devices, \
    dev_to_dict
from adh.exceptions import InvalidIPv4, InvalidIPv6, InvalidMac
from adh.exceptions import MemberNotFound
from adh.model import models
from adh.model.models import Adherent, Modification
from adh.util.session_decorator import require_sql


@require_sql
@auth_regular_admin
def filter_device(limit=100, offset=0, username=None, terms=None):
    """ [API] Filter the list of the devices according to some criterias """
    s = g.session
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
    logging.info("%s fetched the device list", g.admin.login)
    return results, 200, headers


@require_sql
@auth_regular_admin
def put_device(mac_address, body):
    """ [API] Put (update or create) a new device in the database """
    s = g.session

    try:
        wired = is_wired(mac_address, s)
        wireless = is_wireless(mac_address, s)
        wanted_type = body["connectionType"]

        if body["connectionType"] == "wireless" \
                and ('ipAddress' in body or 'ipv6Address' in body):
            return "You cannot assign an IP address to a wireless device", 400

        if wired and wireless:
            if wanted_type == "wired":
                delete_wireless_device(g.admin, mac_address, s)
                device = update_wired_device(g.admin, mac_address, body, s)
                allocate_ip_for_device(s, device, g.admin)
            else:
                delete_wired_device(g.admin, mac_address, s)
                update_wireless_device(g.admin, mac_address, body, s)
            return_code = 204

        elif wired:
            if wanted_type == "wireless":
                delete_wired_device(g.admin, mac_address, s)
                create_wireless_device(g.admin, body, s)
            else:
                device = update_wired_device(g.admin, mac_address, body, s)
                allocate_ip_for_device(s, device, g.admin)
            return_code = 204

        elif wireless:
            if wanted_type == "wired":
                delete_wireless_device(g.admin, mac_address, s)
                device = create_wired_device(g.admin, body, s)
                allocate_ip_for_device(s, device, g.admin)
            else:
                update_wireless_device(g.admin, mac_address, body, s)
            return_code = 204

        else:  # Create device
            if body["mac"] != mac_address:
                return 'The MAC address in the query ' + \
                       'and in the body don\'t match', 400

            if wanted_type == "wired":
                device = create_wired_device(g.admin, body, s)
                allocate_ip_for_device(s, device, g.admin)
            else:
                create_wireless_device(g.admin, body, s)
            return_code = 201

        if return_code == 204:
            logging.info("%s updated the device %s\n%s",
                         g.admin.login, mac_address, json.dumps(body,
                                                                sort_keys=True))

        elif return_code == 201:
            logging.info("%s created the device %s\n%s",
                         g.admin.login, mac_address, json.dumps(body,
                                                                sort_keys=True))

        return NoContent, return_code

    except ip_controller.NoMoreIPAvailable:
        s.rollback()
        return 'No more ip available', 400

    except MemberNotFound:
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


@require_sql
@auth_regular_admin
def get_device(mac_address):
    """ [API] Return the device specified by the macAddress """
    s = g.session

    if is_wireless(mac_address, s):
        q = s.query(models.Portable)
        q = q.filter(models.Portable.mac == mac_address)
        r = q.one()
        logging.info("%s fetched the device %s", g.admin.login, mac_address)
        return dict(r), 200

    elif is_wired(mac_address, s):
        q = s.query(models.Ordinateur)
        q = q.filter(models.Ordinateur.mac == mac_address)
        r = q.one()
        logging.info("%s fetched the device %s", g.admin.login, mac_address)
        return dict(r), 200

    else:
        return NoContent, 404


@require_sql
@auth_regular_admin
def delete_device(mac_address):
    """ [API] Delete the specified device from the database """
    s = g.session

    if is_wireless(mac_address, s):
        delete_wireless_device(g.admin, mac_address, s)
        logging.info("%s deleted the device %s", g.admin.login, mac_address)
        return NoContent, 204

    elif is_wired(mac_address, s):
        delete_wired_device(g.admin, mac_address, s)
        logging.info("%s deleted the device %s", g.admin.login, mac_address)
        return NoContent, 204

    else:
        return NoContent, 404


def allocate_ip_for_device(s, dev, admin):
    if not dev.adherent.date_de_depart or dev.adherent.date_de_depart < datetime.datetime.now().date():
        return  # No need to allocate ip for someone who is not a member

    dev.start_modif_tracking()
    if dev.ipv6 == "En Attente":
        network = dev.adherent.chambre.vlan.adressesv6

        ip_controller.free_expired_devices(s)
        next_ip = ip_controller.get_available_ip(
            network,
            ip_controller.get_all_used_ipv6(s)
        )

        dev.ipv6 = next_ip

    if dev.ip == "En Attente":
        network = dev.adherent.chambre.vlan.adresses

        ip_controller.free_expired_devices(s)
        next_ip = ip_controller.get_available_ip(
            network,
            ip_controller.get_all_used_ipv4(s)
        )

        dev.ip = next_ip

    Modification.add_and_commit(s, dev, admin)
