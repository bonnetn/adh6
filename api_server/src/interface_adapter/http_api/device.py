# coding=utf-8
import requests
from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.device import DeviceType, Device
from src.exceptions import DeviceNotFoundError, NoMoreIPAvailableException
from src.exceptions import UserInputError
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.device_manager import MutationRequest, DeviceManager
from src.util.context import log_extra
from src.util.log import LOG


class DeviceHandler:
    def __init__(self, device_manager: DeviceManager):
        self.device_manager = device_manager

    @with_context
    @require_sql
    @auth_regular_admin
    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, username=None, terms=None):
        """ Filter the list of the devices according to some criterias """
        LOG.debug("http_device_search_called", extra=log_extra(ctx,
                                                               limit=limit,
                                                               offset=offset,
                                                               username=username,
                                                               terms=terms))

        try:
            result, count = self.device_manager.search(ctx, limit, offset, username, terms)

        except UserInputError as e:
            return bad_request(e), 400

        headers = {
            "X-Total-Count": count,
            "access-control-expose-headers": "X-Total-Count"
        }
        return list(map(_map_device_to_http_response, result)), 200, headers

    @with_context
    @require_sql
    @auth_regular_admin
    def put(self, ctx, mac_address, body):
        """ Put (update or create) a new device in the database """
        LOG.debug("http_device_put_called", extra=log_extra(ctx, mac=mac_address, request=body))

        try:
            created = self.device_manager.update_or_create(ctx,
                                                           mac_address=mac_address,
                                                           req=MutationRequest(
                                                               owner_username=body.get('username'),
                                                               mac_address=body.get('mac'),
                                                               connection_type=body.get('connection_type'),
                                                               ip_v4_address=body.get('ip_address'),
                                                               ip_v6_address=body.get('ipv6_address'),
                                                           ),
                                                           )

            if created:
                return NoContent, 201  # 201 Created
            else:
                return NoContent, 204  # 204 No Content

        except NoMoreIPAvailableException:
            return "IP allocation failed.", 503

        except UserInputError as e:
            return bad_request(e), 400

    @with_context
    @require_sql
    @auth_regular_admin
    def get(self, ctx, mac_address):
        """ Return the device specified by the macAddress """
        LOG.debug("http_device_get_called", extra=log_extra(ctx, mac=mac_address))
        try:
            return _map_device_to_http_response(self.device_manager.get_by_mac_address(ctx, mac_address)), 200  # 200 OK

        except DeviceNotFoundError:
            return NoContent, 404  # 404 Not Found

    @with_context
    @require_sql
    @auth_regular_admin
    def delete(self, ctx, mac_address):
        """ Delete the specified device from the database """
        LOG.debug("http_device_delete_called", extra=log_extra(ctx, mac=mac_address))
        try:
            self.device_manager.delete(ctx, mac_address)
            return NoContent, 204

        except DeviceNotFoundError:
            return NoContent, 404

    @with_context
    @require_sql
    @auth_regular_admin
    def vendor_get(self, ctx, mac_address):
        """ Return the vendor associated with the macAddress """
        r = requests.get('https://macvendors.co/api/vendorname/' + str(mac_address))

        if r.status_code == 200:
            LOG.info("vendor_fetch", extra=log_extra(ctx, mac=mac_address))
            return {"vendorname": r.text}, 200

        else:
            return NoContent, 404


def _map_device_to_http_response(device: Device) -> dict:
    con_types = {
        DeviceType.Wired: 'wired',
        DeviceType.Wireless: 'wireless',
    }
    fields = {
        'mac': device.mac_address,
        'ipAddress': device.ip_v4_address,
        'ipv6Address': device.ip_v6_address,
        'connectionType': con_types.get(device.connection_type),
        'username': device.owner_username,
    }
    return {k: v for k, v in fields.items() if v is not None}
