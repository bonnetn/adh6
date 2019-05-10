# coding=utf-8
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql


class TransactionHandler:

    @require_sql
    @auth_regular_admin
    def search(self, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None, account=None):
        pass

    @require_sql
    @auth_regular_admin
    def create_transaction(self, body):
        pass

    @require_sql
    @auth_regular_admin
    def get(self, body):
        pass

    @require_sql
    @auth_regular_admin
    def delete(self, transaction_id):
        pass
