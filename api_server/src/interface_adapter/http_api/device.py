# coding=utf-8
import requests
from connexion import NoContent
from dataclasses import asdict

from main import device_manager
from src.interface_adapter.http_api.decorator.auth import auth_regular_admin
from src.interface_adapter.http_api.decorator.sql_session import require_sql
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.log import LOG
from src.use_case.device_manager import MutationRequest
from src.use_case.exceptions import IntMustBePositiveException, MemberNotFound, IPAllocationFailedError, \
    InvalidMACAddress, InvalidIPAddress, DeviceNotFound
from src.use_case.mutation import Mutation
from src.util.context import log_extra


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=100, offset=0, username=None, terms=None):
    """ Filter the list of the devices according to some criterias """
    LOG.debug("http_device_search_called", extra=log_extra(ctx,
                                                           limit=limit,
                                                           offset=offset,
                                                           username=username,
                                                           terms=terms))

    try:
        result, count = device_manager.search(ctx, limit, offset, username, terms)

    except IntMustBePositiveException as e:
        return bad_request(e), 400

    headers = {
        "X-Total-Count": count,
        "access-control-expose-headers": "X-Total-Count"
    }
    return list(map(asdict, result)), 200, headers


@with_context
@require_sql
@auth_regular_admin
def put(ctx, mac_address, body):
    """ [API] Put (update or create) a new device in the database """
    LOG.debug("http_device_put_called", extra=log_extra(ctx, mac=mac_address, request=body))

    try:
        created = device_manager.update_or_create(ctx,
                                                  mac_address=mac_address,
                                                  req=MutationRequest(
                                                      owner_username=body.get('username', Mutation.NOT_SET),
                                                      mac_address=body.get('mac', Mutation.NOT_SET),
                                                      connection_type=body.get('connectionType', Mutation.NOT_SET),
                                                      ip_v4_address=body.get('ipAddress', Mutation.NOT_SET),
                                                      ip_v6_address=body.get('ipv6Address', Mutation.NOT_SET),
                                                  ),
                                                  )

        if created:
            return NoContent, 201  # 201 Created
        else:
            return NoContent, 204  # 204 No Content
    except IPAllocationFailedError:
        return "IP allocation failed.", 503

    except MemberNotFound:
        return "No member with that username was not found.", 400

    except InvalidMACAddress:
        return "Invalid MAC address.", 400

    except InvalidIPAddress:
        return "Invalid IP address.", 400


@with_context
@require_sql
@auth_regular_admin
def get(ctx, mac_address):
    """ [API] Return the device specified by the macAddress """
    LOG.debug("http_device_get_called", extra=log_extra(ctx, mac=mac_address))
    try:
        return asdict(device_manager.get_by_mac_address(ctx, mac_address)), 200  # 200 OK
    except DeviceNotFound:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def delete(ctx, mac_address):
    """ [API] Delete the specified device from the database """
    LOG.debug("http_device_delete_called", extra=log_extra(ctx, mac=mac_address))
    try:
        device_manager.delete(ctx, mac_address)
        return NoContent, 204
    except DeviceNotFound:
        return NoContent, 404


@with_context
@require_sql
@auth_regular_admin
def get_vendor(ctx, mac_address):
    """ [API] Return the vendor associated with the macAddress """
    r = requests.get('https://macvendors.co/api/vendorname/' + str(mac_address))

    if r.status_code == 200:
        LOG.info("vendor_fetch", extra=log_extra(ctx, mac=mac_address))
        return {"vendorname": r.text}, 200

    else:
        return NoContent, 404
