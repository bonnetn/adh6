"""
AUTHORIZATION MODULE.

What is AuthZ:
> Authorization is the function of specifying access rights/privileges to resources, which is related to information
> security and computer security in general and to access control in particular.

Source: https://en.wikipedia.org/wiki/Authentication
"""
from typing import Optional, Set

from src.controller.jwt_parser import JWTController
from src.entity.api_definition import Policy
from src.entity.configuration import Configuration
from src.gateway.ldap import LDAPGateway
from src.gateway.oidc_server import OIDCServerGateway

AuthRejectMessage = Optional[str]


class AuthorizationController:
    def __init__(self, config: Configuration, gateway: OIDCServerGateway, jwt_parser: JWTController,
                 ldap_gateway: LDAPGateway):
        self.config = config
        self.gateway = gateway
        self.jwt_parser = jwt_parser
        self.ldap_gateway = ldap_gateway

        self._POLICY_TO_FUNCTION = {
            Policy.ALLOW_ALL: self._allow_all,
            Policy.DENY_ALL: self._deny_all,
            Policy.ADMIN_ONLY: self._admin_only,
            Policy.SUPERADMIN_ONLY: self._superadmin_only,
        }

    def is_authorized(self, policy: Policy, token: str) -> (bool, AuthRejectMessage):
        admins = self.ldap_gateway.get_admins()
        superadmins = self.ldap_gateway.get_super_admins()
        return self._POLICY_TO_FUNCTION.get(policy)(token, admins, superadmins)

    def _superadmin_only(self, token: str, admins: Set[str], superadmins: Set[str]) -> (bool, AuthRejectMessage):
        infos = self._parse_token(token)
        return infos['sub'] in superadmins, None

    def _admin_only(self, token: str, admins: Set[str], superadmins: Set[str]) -> (bool, AuthRejectMessage):
        infos = self._parse_token(token)
        return infos['sub'] in admins, None

    def _deny_all(self) -> (bool, AuthRejectMessage):
        return False, 'this endpoint is disallowed for everyone'

    def _allow_all(self) -> (bool, AuthRejectMessage):
        return True, None

    def _parse_token(self, token: str) -> dict:
        key = self.gateway.oidc_jwk_cert()
        return self.jwt_parser.parse(token, key)
