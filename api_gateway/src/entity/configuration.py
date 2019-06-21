from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    PROPAGATE_TO_CLIENT = {"Content-Type"}
    AUTHORIZE_URL = 'https://cas.minet.net:8443/cas/oidc/authorize'
    TOKEN_URL = 'https://cas.minet.net:8443/cas/oidc/accessToken'
    JWK_URL = 'https://cas.minet.net:8443/cas/oidc/jwks'
    REDIRECT_URI = 'https://localhost/api/authorization-code'
    CLIENT_ID = 'adh6_api_gateway'
    CLIENT_SECRET = 'secret'
    VERIFY_CERTS = False
    TIMEOUT = 5

    LDAP_BASE_DN = 'dc=minet,dc=net'
    LDAP_URL = 'ldap://ldap-master.priv.minet.net'
    LDAP_GROUP_ADMIN = 'cn=adh6_user'
    LDAP_GROUP_SUPERADMIN = 'cn=adh6_admin'
    LDAP_CACHE_SECONDS = 60
