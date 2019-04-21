import datetime
import dateutil
import json
import logging
import requests
from connexion import NoContent
from dataclasses import asdict
from flask import g
from sqlalchemy.orm.exc import MultipleResultsFound

from main import device_manager
from src.entity.device import DeviceType
from src.exceptions import InvalidIPv4, InvalidIPv6, InvalidMac
from src.interface_adapter.http_api.decorator.auth import auth_regular_admin
from src.interface_adapter.http_api.decorator.sql_session import require_sql
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.device_utils import is_wired, is_wireless, \
    delete_wireless_device, \
    delete_wired_device, \
    update_wireless_device, \
    update_wired_device, \
    create_wireless_device, \
    create_wired_device, \
    get_all_devices, \
    dev_to_dict
from src.interface_adapter.http_api.util import ip_controller
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.model import models
from src.interface_adapter.sql.model.models import Adherent, Modification
from src.use_case.exceptions import IntMustBePositiveException


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=100, offset=0, username=None, terms=None):
    """ Filter the list of the devices according to some criterias """
    try:
        result, count = device_manager.search(ctx, limit, offset, username, terms)

    except IntMustBePositiveException as e:
        return bad_request(e), 400

    headers = {
        "X-Total-Count": count,
        "access-control-expose-headers": "X-Total-Count"
    }
    return list(map(asdict, result)), 200, headers


@require_sql
@auth_regular_admin
def put(mac_address, body):
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
def get(mac_address):
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
def delete(mac_address):
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


@require_sql
@auth_regular_admin
def get_vendor(mac_address):
    """ [API] Return the vendor associated with the macAddress """
    s = g.session
    r = requests.get('https://macvendors.co/api/vendorname/' + str(mac_address))

    if r.status_code == 200:
        logging.info("%s fetched the vendor for device %s", g.admin.login, mac_address)
        return {"vendorname": r.text}, 200

    else:
        return NoContent, 404


def allocate_ip_for_device(s, dev, admin):
    date_de_depart = dev.adherent.date_de_depart
    if not date_de_depart:
        return

    # Force convertion in date (it can be a datetime or a date)
    date_de_depart = dateutil.parser.parse(str(date_de_depart)).date()
    if not date_de_depart or date_de_depart < datetime.datetime.now().date():
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

    Modification.add(s, dev, admin)
