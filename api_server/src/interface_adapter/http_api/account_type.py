# coding=utf-8
from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account_type import AccountType
from src.exceptions import UserInputError, AccountTypeNotFoundError
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.account_type_manager import AccountTypeManager
from src.util.context import log_extra
from src.util.log import LOG


class AccountTypeHandler:
    def __init__(self, account_type_manager: AccountTypeManager):
        self.account_type_manager = account_type_manager

    @with_context
    @require_sql
    @auth_regular_admin
    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, account_type_id=None, terms=None):
        """ Filter the list of the account type according to some criterias """
        LOG.debug("http_account_type_search_called", extra=log_extra(ctx, limit=limit, offset=offset, terms=terms))

        try:
            result, count = self.account_type_manager.search(ctx, limit=limit, offset=offset,
                                                             account_type_id=account_type_id, terms=terms)

        except UserInputError as e:
            return bad_request(e), 400

        headers = {
            "X-Total-Count": count,
            "access-control-expose-headers": "X-Total-Count"
        }
        return list(map(_map_account_type_to_http_response, result)), 200, headers

    @require_sql
    @auth_regular_admin
    def post(self, body):
        pass

    @with_context
    @require_sql
    @auth_regular_admin
    def get(self, ctx, account_type_id):
        """ Return the account type specified by the id """
        LOG.debug("http_account_type_get_called", extra=log_extra(ctx, account_type_id=account_type_id))
        try:
            result = self.account_type_manager.get_by_id(ctx, account_type_id=account_type_id)
            return _map_account_type_to_http_response(result), 200  # OK

        except AccountTypeNotFoundError:
            return NoContent, 404  # 404 Not Found

    @require_sql
    @auth_regular_admin
    def patch(self, account_type_id, body):
        pass


def _map_account_type_to_http_response(account_type: AccountType) -> dict:
    fields = {
        'account_type_id': account_type.account_type_id,
        'name': account_type.name,
    }
    return {k: v for k, v in fields.items() if v is not None}
