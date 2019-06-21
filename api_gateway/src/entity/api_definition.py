from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet


class Policy(Enum):
    ALLOW_ALL = 'allow_all'
    DENY_ALL = 'deny_all'
    ADMIN_ONLY = 'admin_only'
    SUPERADMIN_ONLY = 'superadmin_only'


@dataclass(frozen=True)
class EndpointDefinition:
    path_regex: str
    authz: Policy
    headers: FrozenSet[str] = field(default_factory=frozenset)
    timeout: float = 5


@dataclass(frozen=True)
class APIDefinition:
    host: str
    cert: str
    endpoints: tuple
