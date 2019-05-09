# coding=utf-8
"""
Contain all the http http_api functions.
"""
from connexion import NoContent
from dataclasses import asdict

from uwsgi_file_main import member_manager
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.member import Member
from src.exceptions import MemberNotFoundError, UserInputError
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.member_manager import FullMutationRequest, PartialMutationRequest
from src.util.context import log_extra
from src.util.int_or_none import int_or_none
from src.util.log import LOG


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None, room_number=None):
    """ Search all the member. """
    LOG.debug("http_member_search_called", extra=log_extra(ctx,
                                                           limit=limit,
                                                           offset=offset,
                                                           terms=terms,
                                                           room_number=room_number))
    try:
        result, total_count = member_manager.search(ctx, limit, offset, room_number, terms)
        headers = {
            "X-Total-Count": str(total_count),
            'access-control-expose-headers': 'X-Total-Count'
        }
        result = list(map(_map_member_to_http_response, result))
        return result, 200, headers  # 200 OK

    except UserInputError as e:
        return bad_request(e), 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def get(ctx, username):
    """ Get a specific member. """
    LOG.debug("http_member_get_called", extra=log_extra(ctx, username=username))
    try:
        return _map_member_to_http_response(member_manager.get_by_username(ctx, username)), 200  # 200 OK

    except MemberNotFoundError:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def delete(ctx, username):
    """ Delete the specified User from the database """
    LOG.debug("http_member_delete_called", extra=log_extra(ctx, username=username))
    try:
        member_manager.delete(ctx, username)
        return NoContent, 204  # 204 No Content

    except MemberNotFoundError:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def patch(ctx, username, body):
    """ Partially update a member from the database """
    LOG.debug("http_member_patch_called", extra=log_extra(ctx, username=username, request=body))
    try:
        mutation_request = _map_http_request_to_partial_mutation_request(body)
        member_manager.update_partially(ctx, username, mutation_request)
        return NoContent, 204  # 204 No Content

    except MemberNotFoundError:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def put(ctx, username, body):
    """ Create/Update member from the database """
    LOG.debug("http_member_put_called", extra=log_extra(ctx, username=username, request=body))

    mutation_request = _map_http_request_to_full_mutation_request(body)
    try:
        created = member_manager.update_or_create(ctx, username, mutation_request)
        if created:
            return NoContent, 201  # 201 Created
        else:
            return NoContent, 204  # 204 No Content

    except UserInputError as e:
        return bad_request(e), 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def post_membership(ctx, username, body):
    """ Add a membership record in the database """
    LOG.debug("http_member_post_membership_called", extra=log_extra(ctx, username=username, request=body))

    try:
        member_manager.new_membership(ctx, username, body.get('duration'), body.get('paymentMethod'),
                                      start_str=body.get('start'))
        return NoContent, 200  # 200 OK

    except MemberNotFoundError:
        return NoContent, 404  # 404 Not Found

    except UserInputError as e:
        return bad_request(e), 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def put_password(ctx, username, body):
    """ Set the password of a member. """
    # Careful not to log the body here!
    LOG.debug("http_member_put_password_called", extra=log_extra(ctx, username=username, body=None))

    try:
        member_manager.change_password(ctx, username, body.get('password'))
        return NoContent, 204  # 204 No Content

    except MemberNotFoundError:
        return NoContent, 404  # 404 Not Found

    except UserInputError as e:
        return bad_request(e), 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def get_logs(ctx, username):
    """ Get logs from a member. """
    LOG.debug("http_member_get_logs_called", extra=log_extra(ctx, username=username))
    try:
        return member_manager.get_logs(ctx, username), 200

    except MemberNotFoundError:
        return NoContent, 404


def _map_member_to_http_response(member: Member) -> dict:
    fields = {
        'email': member.email,
        'firstName': member.first_name,
        'lastName': member.last_name,
        'username': member.username,
        'departureDate': member.departure_date,
        'comment': member.comment,
        'associationMode': member.association_mode,
        'roomNumber': int_or_none(member.room_number),
    }

    return {k: v for k, v in fields.items() if v is not None}


def _map_http_request_to_partial_mutation_request(body) -> PartialMutationRequest:
    return PartialMutationRequest(
        email=body.get('email'),
        first_name=body.get('firstName'),
        last_name=body.get('lastName'),
        username=body.get('username'),
        comment=body.get('comment'),
        departure_date=body.get('departureDate'),
        association_mode=body.get('associationMode'),
        room_number=body.get('roomNumber'),
    )


def _map_http_request_to_full_mutation_request(body) -> FullMutationRequest:
    partial = _map_http_request_to_partial_mutation_request(body)
    return FullMutationRequest(**asdict(partial))
