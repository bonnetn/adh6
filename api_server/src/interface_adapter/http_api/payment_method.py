# coding=utf-8
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql


@require_sql
@auth_regular_admin
def search(limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None):
    pass


@require_sql
@auth_regular_admin
def post(body):
    pass


@require_sql
@auth_regular_admin
def get(payment_method_id):
    pass


@require_sql
@auth_regular_admin
def patch(payment_method_id, body):
    pass
