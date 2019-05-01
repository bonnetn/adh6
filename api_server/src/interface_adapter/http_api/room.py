# coding=utf-8
from connexion import NoContent

from main import room_manager
from src.entity.room import Room
from src.exceptions import RoomNotFound, VlanNotFound
from src.interface_adapter.http_api.decorator.auth import auth_regular_admin, auth_super_admin
from src.interface_adapter.http_api.decorator.sql_session import require_sql
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.use_case.room_manager import MutationRequest
from src.use_case.util.exceptions import IntMustBePositiveException, MissingRequiredFieldError, RoomNumberMismatchError
from src.util.context import log_extra
from src.util.log import LOG


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=100, offset=0, terms=None):
    """ Filter the list of the rooms """
    LOG.debug("http_room_search_called", extra=log_extra(ctx, terms=terms))
    try:
        result, count = room_manager.search(ctx, limit=limit, offset=offset, terms=terms)
        result = map(_map_room_to_http_response, result)
        result = list(result)
        headers = {
            'access-control-expose-headers': 'X-Total-Count',
            'X-Total-Count': str(count)
        }
        return result, 200, headers

    except IntMustBePositiveException as e:
        return bad_request(e), 400


@with_context
@require_sql
@auth_super_admin
def put(ctx, room_number, body):
    """ Update/create a room in the database """
    LOG.debug("http_room_put_called", extra=log_extra(ctx, room_manager=room_manager, request=body))
    try:
        created = room_manager.update_or_create(ctx, room_number, MutationRequest(
            room_number=body.get('roomNumber'),
            description=body.get('description'),
            phone_number=body.get('phone'),
            vlan_number=body.get('vlan'),
        ))
    except (MissingRequiredFieldError, VlanNotFound, RoomNumberMismatchError) as e:
        return bad_request(e), 400

    if created:
        return NoContent, 201
    else:
        return NoContent, 204


@with_context
@require_sql
@auth_regular_admin
def get(ctx, room_number):
    """ Get the room specified """
    LOG.debug("http_room_get_called", extra=log_extra(ctx, room_number=room_number))
    try:
        result = room_manager.get_by_number(ctx, room_number)
        return _map_room_to_http_response(result), 200

    except RoomNotFound:
        return NoContent, 404


@with_context
@require_sql
@auth_super_admin
def delete(ctx, room_number):
    """ Delete room from the database """
    LOG.debug("http_room_delete_called", extra=log_extra(ctx, room_number=room_number))
    try:
        room_manager.delete(ctx, room_number)
        return NoContent, 204

    except RoomNotFound:
        return NoContent, 404


def _map_room_to_http_response(room: Room) -> dict:
    fields = {
        'description': room.description,
        'roomNumber': int(room.room_number),
        'phone': int(room.phone_number),
        'vlan': int(room.vlan_number),
    }
    return {k: v for k, v in fields.items() if v is not None}
