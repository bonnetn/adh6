# coding=utf-8
from connexion import NoContent

from main import port_manager
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.port import Port
from src.exceptions import SwitchNotFound, PortNotFound, RoomNotFound, IntMustBePositiveException
from src.interface_adapter.sql.decorator.auth import auth_regular_admin, auth_super_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.use_case.port_manager import MutationRequest
from src.util.context import log_extra
from src.util.int_or_none import int_or_none
from src.util.log import LOG


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, switch_id=None, room_number=None, terms=None):
    """ Filter the port list according to some criteria """
    LOG.debug("http_port_search_called",
              extra=log_extra(ctx, switch_id=switch_id, room_number=room_number, terms=terms))

    try:
        result, count = port_manager.search(ctx, limit=limit, offset=offset, switch_id=switch_id,
                                            room_number=room_number,
                                            terms=terms)
    except IntMustBePositiveException as e:
        return bad_request(e), 400

    headers = {
        'access-control-expose-headers': 'X-Total-Count',
        'X-Total-Count': str(count)
    }
    return list(map(_map_port_to_http_response, result)), 200, headers


@with_context
@require_sql
@auth_super_admin
def post(ctx, body):
    """ Create a port in the database """
    LOG.debug("http_port_post_called", extra=log_extra(ctx, request=body))

    try:
        port_id = port_manager.create(ctx, MutationRequest(
            port_number=body.get('portNumber'),
            room_number=body.get('roomNumber'),
            switch_id=body.get('switchID'),
        ))

    except RoomNotFound:
        return 'Invalid room number.', 400

    except SwitchNotFound:
        return 'Invalid switch ID.', 400

    headers = {'Location': '/port/{}'.format(port_id)}
    return NoContent, 200, headers


@with_context
@require_sql
@auth_regular_admin
def get(ctx, port_id):
    """ Get a port from the database """
    LOG.debug("http_port_get_called", extra=log_extra(ctx, port_id=port_id))

    result, count = port_manager.search(ctx, port_id=port_id)
    if not result:
        return NoContent, 404

    return _map_port_to_http_response(result[0]), 200


@with_context
@require_sql
@auth_super_admin
def put(ctx, port_id, body):
    """ Update a port in the database """
    LOG.debug("http_port_put_called", extra=log_extra(ctx, port_id=port_id))

    try:
        port_manager.update(ctx, MutationRequest(
            port_id=port_id,
            port_number=body.get('portNumber'),
            room_number=body.get('roomNumber'),
            switch_id=body.get('switchID'),
        ))

    except PortNotFound:
        return NoContent, 404

    except RoomNotFound:
        return 'Invalid room number', 400

    except SwitchNotFound:
        return 'Invalid switch ID', 400

    return NoContent, 204


@with_context
@require_sql
@auth_super_admin
def delete(ctx, port_id):
    """ Delete a port from the database """
    LOG.debug("http_port_delete_called", extra=log_extra(ctx, port_id=port_id))
    try:
        port_manager.delete(ctx, port_id)
    except PortNotFound:
        return NoContent, 404

    return NoContent, 204


@auth_regular_admin
def get_state(switchID, port_id):
    return NoContent, 501, True


@auth_regular_admin
def put_state(switchID, port_id, state):
    return NoContent, 501


@auth_regular_admin
def get_vlan(switchID, port_id):
    return NoContent, 501, 42


@auth_regular_admin
def put_vlan(switchID, port_id, vlan):
    return NoContent, 501


@auth_regular_admin
def get_mab(port_id):
    return False, 501


@auth_regular_admin
def put_mab(port_id, mab):
    return NoContent, 501


def _map_port_to_http_response(port: Port) -> dict:
    fields = {
        'id': int_or_none(port.id),
        'portNumber': port.port_number,
        'roomNumber': int_or_none(port.room_number),
        'switchID': int_or_none(port.switch_info.switch_id),
    }
    return {k: v for k, v in fields.items() if v is not None}
