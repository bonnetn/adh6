# coding=utf-8
"""
Auth decorators.
"""
import datetime
from connexion import NoContent
from sqlalchemy.orm.exc import NoResultFound

from src.constants import CTX_TESTING, CTX_SQL_SESSION
from src.entity.admin import Admin
from src.interface_adapter.http_api.auth import ADH6_USER, ADH6_ADMIN
from src.interface_adapter.sql.model.models import Utilisateur
from src.util.context import build_context, log_extra
from src.util.log import LOG


def _find_admin(s, username):
    """
    Get the specified admin, if it does not exist, create it.

    The SQL table 'Utilisateur' is not the source of truth for all the admins. That means that it is populated just so
    we can use admin_id for the entries. This table is not used for access control at all!

    This means when a new admin connects to ADH, she/he is not in the table yet, and we must create it. Here we also
    assume that the admin is authenticated before this function is called.

    """
    try:
        q = s.query(Utilisateur)
        q = q.filter(Utilisateur.login == username)
        return q.one()

    except NoResultFound:
        now = datetime.datetime.now()
        new_admin = Utilisateur(
            nom="-",
            access=42,
            email="-",
            login=username,
            password_hash="-",
            created_at=now,
            updated_at=now,
            access_token="-"
        )
        s.add(new_admin)
        return new_admin


def auth_regular_admin(f):
    """
    Authenticate a regular admin.
    """

    # @wraps(f) # Cannot wrap this function, because connexion needs to know we have the user and token_info...
    def wrapper(cls, ctx, *args, user, token_info, **kwargs):
        """
        Wrap http_api function.
        """
        if not ctx.get(CTX_TESTING) and (user is None or token_info is None):
            LOG.warning('could_not_extract_user_and_token_info_kwargs', extra=log_extra(ctx))
            return NoContent, 401

        if not ctx.get(CTX_TESTING) and ADH6_USER not in token_info["groups"]:
            # User is not in the right group and we are not testing, do not allow.
            return NoContent, 401

        assert ctx.get(CTX_SQL_SESSION) is not None, 'You need SQL for authentication.'
        admin = _find_admin(ctx.get(CTX_SQL_SESSION), user)
        ctx = build_context(ctx=ctx, admin=Admin(login=admin.login))
        return f(cls, ctx, *args, **kwargs)  # Discard the user and token_info.

    return wrapper


def auth_super_admin(f):
    """
    Authenticate a super admin.
    """

    def wrapper(cls, ctx, *args, user, token_info, **kwargs):
        """
        Wrap http_api function.
        """
        if not ctx.get(CTX_TESTING) and ADH6_ADMIN not in token_info["groups"]:
            # User is not in the right group and we are not testing, do not allow.
            return NoContent, 401

        admin = _find_admin(ctx.get(CTX_SQL_SESSION), user)
        ctx = build_context(ctx=ctx, admin=Admin(login=admin.login))
        return f(cls, ctx, *args, **kwargs)  # Discard the user and token_info.

    return wrapper
