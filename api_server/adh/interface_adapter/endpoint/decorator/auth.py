import logging
from functools import wraps

from connexion import NoContent

from adh.constants import CTX_TESTING, CTX_SQL_SESSION
from adh.interface_adapter.endpoint.auth import ADH6_USER, ADH6_ADMIN
from adh.interface_adapter.sql.model.models import Utilisateur
from adh.util.context import build_context


def auth_regular_admin(f):
    # @wraps(f) # Cannot wrap this function, because connexion needs to know we have the user and token_info...
    def wrapper(ctx, *args, user, token_info, **kwargs):
        if not ctx.get(CTX_TESTING) and (user is None or token_info is None):
            logging.warn('Could not extract user and token_info kwargs.')
            return NoContent, 401

        if not ctx.get(CTX_TESTING) and ADH6_USER not in token_info["groups"]:
            # User is not in the right group and we are not testing, do not allow.
            return NoContent, 401

        assert ctx.get(CTX_SQL_SESSION) is not None, 'You need SQL for authentication.'
        admin = Utilisateur.find_or_create(ctx.get(CTX_SQL_SESSION), user)  # TODO: remove dep from sqlalchemy...
        ctx = build_context(ctx=ctx, admin=admin)
        return f(ctx, *args, **kwargs)  # Discard the user and token_info.

    return wrapper


def auth_super_admin(f):
    def wrapper(ctx, *args, user, token_info, **kwargs):
        print('auth', kwds)
        if not ctx.get(CTX_TESTING) and ADH6_ADMIN not in token_info["groups"]:
            # User is not in the right group and we are not testing, do not allow.
            return NoContent, 401

        admin = Utilisateur.find_or_create(ctx.get(CTX_SQL_SESSION), user)
        ctx = build_context(ctx=ctx, admin=admin)
        return f(ctx, *args, **kwargs)  # Discard the user and token_info.

    return wrapper
