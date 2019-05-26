# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.product import Product
from src.exceptions import ProductNotFoundError
from src.interface_adapter.sql.model.models import Product as SQLProduct
from src.interface_adapter.sql.track_modifications import track_modifications
from src.use_case.interface.product_repository import ProductRepository
from src.util.context import log_extra
from src.util.log import LOG


class ProductSQLRepository(ProductRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_product(self, ctx, name=None, selling_price=None, buying_price=None):
        """
        Create a product .

        :raise ProductTypeNotFound ?
        """

        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_product_repository_create_product_called", extra=log_extra(ctx, name=name))

        product = SQLProduct(
            name=name,
            buying_price=buying_price,
            selling_price=selling_price,
        )

        with track_modifications(ctx, s, product):
            s.add(product)

        return product

    # TODO: update_account mais même problème qu'au dessus

    def search_product_by(self, ctx, limit=None, offset=None, product_id=None, terms=None) -> (List[Product], int):
        """
        Search for a product.
        """
        LOG.debug("sql_product_repository_search_called", extra=log_extra(ctx, product_id=product_id, terms=terms))
        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SQLProduct)

        if product_id:
            q = q.filter(SQLProduct.id == product_id)
        if terms:
            q = q.filter(SQLProduct.name.contains(terms))

        count = q.count()
        #q = q.order_by(SQLProduct.creation_date.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_product_sql_to_entity, r)), count

    def update_product(self, ctx, name=None, selling_price=None, buying_price=None, product_id=None) -> None:
        """
        Update a product.
        Will raise (one day) ProductNotFound
        """
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_product_repository_update_product_called", extra=log_extra(ctx, product_id=product_id))

        product = _get_product_by_id(s, product_id)
        if product is None:
            raise ProductNotFoundError(product_id)

        with track_modifications(ctx, s, product):
            product.name = name or product.name
            product.buying_price = buying_price or product.buying_price
            product.selling_price = selling_price or product.selling_price

    def delete_product(self, ctx, name=None):
        """
        Delete a product.

        :raise ProductNotFound (one day)
        """
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_product_repository_delete_product_called", extra=log_extra(ctx, name=name))

        # Find the soon-to-be deleted user
        product = _get_product_by_name(s, name)
        if not product:
            raise ProductNotFoundError(name)

        with track_modifications(ctx, s, product):
            # Actually delete it
            s.delete(product)


def _map_product_sql_to_entity(p) -> Product:
    """
    Map a Product object from SQLAlchemy to a Product (from the entity folder/layer).
    """
    return Product(
        name=p.name,
        buying_price=p.buying_price,
        selling_price=p.selling_price,
        product_id=p.id
    )


def _get_product_by_id(s, id) -> SQLProduct:
    return s.query(SQLProduct).filter(SQLProduct.id == id).one_or_none()


def _get_product_by_name(s, name) -> Product:
    return s.query(Product).filter(Product.name == name).one_or_none()