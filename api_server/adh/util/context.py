from types import MappingProxyType

from adh.constants import CTX_SQL_SESSION, CTX_ADMIN, CTX_TESTING


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
