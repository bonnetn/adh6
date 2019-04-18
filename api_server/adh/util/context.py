from types import MappingProxyType

from adh.constants import CTX_SQL_SESSION, CTX_ADMIN


def build_context(session=None, admin=None):
    return MappingProxyType({
        CTX_SQL_SESSION: session,
        CTX_ADMIN: admin,
    })
