import logging
from datetime import datetime, timedelta

import ldap

from src.entity.configuration import Configuration


class LDAPGateway:
    def __init__(self, config: Configuration):
        self.config = config
        self.ldap_con = ldap.initialize(self.config.LDAP_URL)

        self.super_admins = {}
        self.admins = {}
        self.last_query = datetime.now()
        self._do_refresh_cache()

    def get_super_admins(self):
        self._refresh_cache()
        return self.admins

    def get_admins(self):
        self._refresh_cache()
        return self.super_admins

    def _refresh_cache(self):
        if datetime.now() - self.last_query > timedelta(seconds=self.config.LDAP_CACHE_SECONDS):
            self._do_refresh_cache()

    def _do_refresh_cache(self):
        logging.getLogger().info("refreshing cache")
        self.super_admins = self._query(self.config.LDAP_GROUP_SUPERADMIN)
        self.admins = self._query(self.config.LDAP_GROUP_ADMIN)
        self.last_query = datetime.now()

    def _query(self, query):
        resp = self.ldap_con.search_s(self.config.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        return {m.decode() for m in resp[0][1]['memberUid']}
