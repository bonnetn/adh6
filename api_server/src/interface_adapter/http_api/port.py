# coding=utf-8
from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.port import Port
from src.exceptions import PortNotFoundError, UserInputError
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin, auth_super_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.port_manager import MutationRequest, PortManager
from src.util.context import log_extra
from src.util.int_or_none import int_or_none
from src.util.log import LOG


class PortHandler:
    def __init__(self, port_manager: PortManager):
        self.port_manager = port_manager

    @with_context
    @require_sql
    @auth_regular_admin
    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, switch_id=None, room_number=None, terms=None):
        """ Filter the port list according to some criteria """
        LOG.debug("http_port_search_called",
                  extra=log_extra(ctx, switch_id=switch_id, room_number=room_number, terms=terms))

        try:
            result, count = self.port_manager.search(ctx, limit=limit, offset=offset, switch_id=switch_id,
                                                     room_number=room_number,
                                                     terms=terms)
            headers = {
                'access-control-expose-headers': 'X-Total-Count',
                'X-Total-Count': str(count)
            }
            return list(map(_map_port_to_http_response, result)), 200, headers

        except UserInputError as e:
            return bad_request(e), 400

    @with_context
    @require_sql
    @auth_super_admin
    def post(self, ctx, body):
        """ Create a port in the database """
        LOG.debug("http_port_post_called", extra=log_extra(ctx, request=body))

        try:
            port_id = self.port_manager.create(ctx, MutationRequest(
                port_number=body.get('port_number'),
                room_number=body.get('room_number'),
                switch_id=body.get('switch_id'),
                rcom=0,  # TODO: Add to spec.
                oid=None,  # TODO: Add to spec.
            ))

            headers = {'Location': '/port/{}'.format(port_id)}
            return NoContent, 200, headers

        except UserInputError as e:
            return bad_request(e), 400

    @with_context
    @require_sql
    @auth_regular_admin
    def get(self, ctx, port_id):
        """ Get a port from the database """
        LOG.debug("http_port_get_called", extra=log_extra(ctx, port_id=port_id))

        result, count = self.port_manager.search(ctx, port_id=port_id)  # TODO: Make a use case for that.
        if not result:
            return NoContent, 404

        return _map_port_to_http_response(result[0]), 200

    @with_context
    @require_sql
    @auth_super_admin
    def put(self, ctx, port_id, body):
        """ Update a port in the database """
        LOG.debug("http_port_put_called", extra=log_extra(ctx, port_id=port_id))

        try:
            self.port_manager.update(ctx, port_id, MutationRequest(
                port_number=body.get('port_number'),
                room_number=body.get('room_number'),
                switch_id=body.get('switch_id'),
                rcom=0,  # Add to spec.
                oid=None,  # Add to spec.
            ))
            return NoContent, 204

        except PortNotFoundError:
            return NoContent, 404

        except UserInputError as e:
            return bad_request(e), 400

    @with_context
    @require_sql
    @auth_super_admin
    def delete(self, ctx, port_id):
        """ Delete a port from the database """
        LOG.debug("http_port_delete_called", extra=log_extra(ctx, port_id=port_id))
        try:
            self.port_manager.delete(ctx, port_id)
            return NoContent, 204

        except PortNotFoundError:
            return NoContent, 404

    @auth_regular_admin
    def state_get(self, switchID, port_id):
        return NoContent, 501, True

    @auth_regular_admin
    def state_put(self, switchID, port_id, state):
        return NoContent, 501

    @auth_regular_admin
    def vlan_get(self, switchID, port_id):
        return NoContent, 501, 42

    @auth_regular_admin
    def vlan_put(self, switchID, port_id, vlan):
        return NoContent, 501

    @auth_regular_admin
    def mab_get(self, port_id):
        return False, 501

    @auth_regular_admin
    def mab_put(self, port_id, mab):
        return NoContent, 501


def _map_port_to_http_response(port: Port) -> dict:
    fields = {
        'id': int_or_none(port.id),
        'portNumber': port.port_number,
        'roomNumber': int_or_none(port.room_number),
        'switchID': int_or_none(port.switch_info.switch_id),
    }
    return {k: v for k, v in fields.items() if v is not None}
