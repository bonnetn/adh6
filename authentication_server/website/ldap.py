import ldap
import logging
import ldap.filter
from CONFIGURATION import LDAP_CONF


class UserNotFound(Exception):
    pass


class LdapServ():

    @staticmethod
    def __init_ldap_con():
            # Force nice LDAP over TLS with CA
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_HARD)
            ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, LDAP_CONF["ca_file"])
            ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)

            ldapObj = ldap.initialize(LDAP_CONF["host"])
            ldapObj.protocol_version = ldap.VERSION3
            return ldapObj

    @staticmethod
    def __find_cn(nickname, ldapObj):
        nickname = ldap.filter.escape_filter_chars(nickname)
        ldapObj.simple_bind(
            "cn={},dc=minet,dc=net".format(LDAP_CONF["cn_anonymous"]),
            LDAP_CONF["pass_anonymous"]
        )

        baseDN = LDAP_CONF["base_dn"]
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "uid=" + nickname

        ldap_result_id = ldapObj.search(baseDN, searchScope, searchFilter,
                                        retrieveAttributes)
        result_type = None
        result_data = True
        while result_data and result_type != ldap.RES_SEARCH_ENTRY:
            result_type, result_data = ldapObj.result(ldap_result_id, 0)

        if not result_data:
            raise UserNotFound()

        return result_data[0][0]

    @staticmethod
    def __try_to_connect(dn, password, ldapObj):
        try:
            ldapObj.simple_bind_s(dn, password)
            return True
        except Exception:
            return False

    @staticmethod
    def login(username, password):
        username = ldap.filter.escape_filter_chars(username)
        try:
            ldapObj = LdapServ.__init_ldap_con()
            dn = LdapServ.__find_cn(username, ldapObj)
            return LdapServ.__try_to_connect(dn, password, ldapObj)
        except Exception as e:
            logging.exception("Could not connect to LDAP "
                              "to check the credentials")
            return False

    @staticmethod
    def find_groups(username):
        username = ldap.filter.escape_filter_chars(username)
        ldapObj = LdapServ.__init_ldap_con()
        search_filter = '(|(&(objectClass=*)(memberUid=%s)))' % username
        try:
            results = ldapObj.search_s("ou=groups,dc=minet,dc=net",
                                       ldap.SCOPE_SUBTREE, search_filter,
                                       attrlist=['cn'])
            return list(map(lambda x: x[1]['cn'][0].decode(), results))
        except ldap.NO_SUCH_OBJECT as e:
            return False
        except Exception as e:
            return False
        return False
