# coding=utf-8
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql

from src.entity.product import Product
from src.use_case.product_manager import ProductManager


class ProductHandler:
    def __init__(self, product_manager: ProductManager):
        self.product_manager = product_manager

    @require_sql
    @auth_regular_admin
    def search(self, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None):
        # TODO: LOG.debug
        try:
            result, count = self.product_manager.get_by_name(ctx, limit, offset, name, terms)
        except Exception:
            pass
        # TODO: except NameInputError

        headers = {
            "X-Total-Count": count,
            "access-control-expose-headers": "X-Total-Count"
        }
        return list(map(_map_product_to_http_response, result)), 200, headers

    @require_sql
    @auth_regular_admin
    def post(self, body):
        pass

    @require_sql
    @auth_regular_admin
    def get(self, product_id):
        pass

    @require_sql
    @auth_regular_admin
    def patch(self, product_id, body):
        pass


def _map_account_to_http_response(product: Product) -> dict:
    fields = {
        'name': product.name,
        'buying_price': product.buying_price,
        'selling_price': product.selling_price,
    }
    return {k: v for k, v in fields.items() if v is not None}