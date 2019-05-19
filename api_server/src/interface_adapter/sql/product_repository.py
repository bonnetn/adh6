# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.product import Product
from src.use_case.interface.product_repository import ProductRepository

# TODO: update_product mais même problème qu'au dessus
# TODO: delete_product


class ProductSQLRepository(ProductRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_product(self, ctx, name=None, buying_price=None, selling_price=None) -> None:
        """
        Create a product.
        Possibly raise nothing ?

        s = ctx.get(CTX_SQL_SESSION)

        TODO: LOG.debug

        product = Product(
                name=name,
                buying_price=buying_price,
                selling_price=selling_price)
        """
        pass

        # TODO: voir si track_modifications prendre en compte product et si s.add(product) fonctionne

    def search_product_by(self, ctx, limit=None, offset=None, name=None, terms=None) -> \
            (List[Product], int):
        """
        Search for a product.
        """
        pass

    def update_product(self, ctx, product_to_update, name=None, buying_price=None, selling_price=None):
        """
        Update a product.

        :raise ProductNotFound (one day)
        """
        pass

    def delete_product(self, ctx, name=None):
        """
        Delete a product.

        :raise ProductNotFound (one day)
        """
        pass


def _map_product_sql_to_entity(p) -> Product:
    """
    Map a Product object from SQLAlchemy to a Product (from the entity folder/layer).
    """
    return Product(
        name=p.name,
        selling_price=p.selling_price,
        buying_price=p.buying_price
    )
