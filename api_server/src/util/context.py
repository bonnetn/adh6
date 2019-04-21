from types import MappingProxyType

from src.constants import CTX_SQL_SESSION, CTX_ADMIN, CTX_TESTING


def build_context(ctx: MappingProxyType = None, session=None, admin=None, testing=None):
    """

    :rtype:
    """
    new_fields = {
        CTX_SQL_SESSION: session,
        CTX_ADMIN: admin,
        CTX_TESTING: testing,
    }
    if ctx is None:
        return MappingProxyType(new_fields)

    old_fields = {k: v for k, v in ctx.items() if v is not None}  # Remove None fields.

    merged = {**new_fields, **old_fields}  # Merge old and new context, with priority for the new one.

    return MappingProxyType(merged)


def build_log_extra(context: MappingProxyType, **extra_fields):
    admin_login = None
    if context.get(CTX_ADMIN):
        admin_login = context.get(CTX_ADMIN).login

    infos = {
        'admin': admin_login,
        'testing': str(context.get(CTX_TESTING) or False),
    }
    return {
        'extra': {**infos, **extra_fields},
    }
