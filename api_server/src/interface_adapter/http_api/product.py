# coding=utf-8
from dataclasses import asdict

from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.product import Product
from src.exceptions import ProductNotFoundError, UserInputError
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.product_manager import PartialMutationRequest, ProductManager, FullMutationRequest
from src.util.context import log_extra
from src.util.log import LOG


class ProductHandler:
    def __init__(self, product_manager: ProductManager):
        self.product_manager = product_manager

    @with_context
    @require_sql
    @auth_regular_admin
    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None):

        LOG.debug("http_product_search_called", extra=log_extra(ctx,
                                                                limit=limit,
                                                                offset=offset,
                                                                terms=terms))
        try:
            result, count = self.product_manager.search(ctx, product_id=None, terms=terms)
            headers = {
                "X-Total-Count": count,
                'access-control-expose-headers': 'X-Total-Count'
            }
            return list(map(_map_product_to_http_response, result)), 200, headers

        except UserInputError as e:
            return bad_request(e), 400  # 400 Bad Request

    @with_context
    @require_sql
    @auth_regular_admin
    def post(self, ctx, body):
        """ Add a product record in the database """
        LOG.debug("http_product_post_called", extra=log_extra(ctx, request=body))

        try:
            created = self.product_manager.update_or_create(ctx, req=FullMutationRequest(
                                                            name=body.get('name'),
                                                            buying_price=body.get('buying_price'),
                                                            selling_price=body.get('selling_price')),
                                                            product_id=body.get('id_'))
            if created:
                return NoContent, 201  # 201 Created
            else:
                return NoContent, 204  # 204 No Content

        except UserInputError as e:
            return bad_request(e), 400  # 400 Bad Request

    @with_context
    @require_sql
    @auth_regular_admin
    def get(self, ctx, product_id):
        """ Get a specific account. """
        LOG.debug("http_product_get_called", extra=log_extra(ctx, product_id=product_id))
        try:
            result = self.product_manager.get_by_id(ctx, product_id)
            return _map_product_to_http_response(result), 200  # 200 OK
        except ProductNotFoundError:
            return NoContent, 404  # 404 Not Found

    @with_context
    @require_sql
    @auth_regular_admin
    def delete(self, ctx, name):
        """ Delete the specified Product from the database """
        LOG.debug("http_product_delete_called", extra=log_extra(ctx, name=name))
        try:
            self.product_manager.delete(ctx, name)
            return NoContent, 204  # 204 No Content

        except ProductNotFoundError:
            return NoContent, 404  # 404 Not Found

    @with_context
    @require_sql
    @auth_regular_admin
    def patch(self, ctx, product_id, body):
        """ Partially update a product from the database """
        LOG.debug("http_product_patch_called", extra=log_extra(ctx, product_id=body.get("id_"), request=body))
        try:
            mutation_request = _map_http_request_to_full_mutation_request(body)
            self.product_manager.update_or_create(ctx, mutation_request, body.get("id_"))
            return NoContent, 204  # 204 No Content

        except ProductNotFoundError:
            return NoContent, 404  # 404 Not Found


def _map_http_request_to_partial_mutation_request(body) -> PartialMutationRequest:
    return PartialMutationRequest(
        name=body.get('name'),
        selling_price=body.get('selling_price'),
        buying_price=body.get('buying_price'),
    )


def _map_product_to_http_response(product: Product) -> dict:
    fields = {
        'name': product.name,
        'buying_price': product.buying_price,
        'selling_price': product.selling_price,
        'id': product.product_id,
    }
    return {k: v for k, v in fields.items() if v is not None}


def _map_http_request_to_full_mutation_request(body) -> FullMutationRequest:
    partial = _map_http_request_to_partial_mutation_request(body)
    return FullMutationRequest(**asdict(partial))


