from connexion import NoContent

from adh.exceptions import MemberNotFound
from adh.interface_adapter.endpoint.decorator.auth import auth_regular_admin
from adh.interface_adapter.endpoint.decorator.with_context import with_context
from adh.interface_adapter.endpoint.decorator.sql_session import require_sql
from adh.use_case.member_manager import MutationRequest, Mutation
from adh.util.date import string_to_date
from main import member_manager


@with_context
@require_sql
@auth_regular_admin
def search(ctx, limit=100, offset=0, terms=None, roomNumber=None):
    """ [API] Filter the list of members from the the database """
    try:
        result, total_count = member_manager.search(ctx, limit, offset, roomNumber, terms)
        headers = {
            "X-Total-Count": str(total_count),
            'access-control-expose-headers': 'X-Total-Count'
        }
        return result, 200, headers  # 200 OK
    except ValueError as e:
        return f'Wrong argument: {e}.', 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def get(ctx, username):
    """ [API] Get the specified member from the database """
    try:
        return member_manager.get_by_username(ctx, username), 200
    except MemberNotFound:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def delete(ctx, username):
    """ [API] Delete the specified User from the database """
    try:
        member_manager.delete(ctx, username)
        return NoContent, 204  # 204 No Content

    except MemberNotFound:
        return NoContent, 404  # 404 Not Found


@with_context
@require_sql
@auth_regular_admin
def patch(ctx, username, body):
    """ [API] Partially update a member from the database """
    try:
        mutation_request = _build_mutation_request_from_body(body)
        member_manager.update_partially(ctx, username, mutation_request)
        return NoContent, 204  # 204 No Content

    except MemberNotFound:
        return NoContent, 404  # 404 Not Found

    except ValueError as e:
        return f"Invalid parameter: {e}", 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def put(ctx, username, body):
    """ [API] Create/Update member from the database """
    mutation_request = _build_mutation_request_from_body(body)
    try:
        created = member_manager.create_or_update(ctx, username, mutation_request)
        if created:
            return NoContent, 201  # 201 Created
        else:
            return NoContent, 204  # 204 No Content
    except ValueError as e:
        return f"Invalid parameter: {e}", 400  # 400 Bad Request


@with_context
@require_sql
@auth_regular_admin
def post_membership(ctx, username, body):
    """ Add a membership record in the database """
    try:
        member_manager.new_membership(ctx, username, body.get('duration'), start_str=body.get('start'))
    except MemberNotFound:
        return NoContent, 404  # 404 Not Found
    except ValueError as e:
        return f'Wrong argument: {e}.', 400  # 400 Bad Request

    return NoContent, 200  # 200 OK


@with_context
@require_sql
@auth_regular_admin
def put_password(ctx, username, body):
    try:
        member_manager.change_password(ctx, username, body.get('password'))
    except MemberNotFound:
        return NoContent, 404  # 404 Not Found
    except ValueError as e:
        return f"Wrong argument: {e}", 400  # 400 Bad Request

    return NoContent, 204  # 204 No Content


@with_context
@require_sql
@auth_regular_admin
def get_logs(ctx, username):
    try:
        return member_manager.get_logs(ctx, username), 200
    except MemberNotFound:
        return NoContent, 404
    except ValueError:
        return NoContent, 400


def _string_to_date_or_unset(d):
    if d is None:
        return Mutation.NOT_SET

    if isinstance(d, str):
        return string_to_date(d)

    return d


def _build_mutation_request_from_body(body) -> MutationRequest:
    return MutationRequest(
        email=body.get('email', Mutation.NOT_SET),
        first_name=body.get('firstName', Mutation.NOT_SET),
        last_name=body.get('lastName', Mutation.NOT_SET),
        username=body.get('username', Mutation.NOT_SET),
        departure_date=_string_to_date_or_unset(body.get('departureDate')),
        comment=body.get('comment', Mutation.NOT_SET),
        association_mode=_string_to_date_or_unset(body.get('associationMode')),
        room_number=body.get('roomNumber', Mutation.NOT_SET),
    )
