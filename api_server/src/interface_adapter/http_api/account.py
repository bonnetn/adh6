# coding=utf-8
import requests
from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
#from src.use_case.account_manager import AccountManager

class AccountHandler:
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager

    @require_sql
    @auth_regular_admin
    def search(self, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None):
        #TODO: LOG.debug
        try:
            result, count = self.account_manager.get_by_name(ctx, limit, offset, name, terms)

        #TODO: except NameInputError

        headers = {
            "X-Total-Count": count,
            "access-control-expose-headers": "X-Total-Count"
        }
        return list(map(_map_account_to_http_response, result)), 200, headers


    @require_sql
    @auth_regular_admin
    def post(self, body):
        pass

    @require_sql
    @auth_regular_admin
    def get(self, account_id):
        pass

    @require_sql
    @auth_regular_admin
    def patch(self, account_id, body):
        pass
