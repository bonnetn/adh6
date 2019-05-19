from typing import List

from src.entity.product import Product
from src.use_case.interface.product_repository import ProductRepository

from src.exceptions import IntMustBePositive

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET


# TODO: class MutationRequest(Product) pour modifier un produit et lever les différentes erreurs ?
# TODO: update_or_create


class ProductManager:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_by_name(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, name=None, terms=None) -> \
            (List[Product], int):
        """
        Search a product in the database.
        """
        if limit < 0:
            raise IntMustBePositive('limit')
        if offset < 0:
            raise IntMustBePositive('limit')

        result, count = self.account_repository.search_account_by(ctx, limit=limit, offset=offset, name=name,
                                                                  terms=terms)

        # TODO: LOG.info

        return result, count

    def delete(self, ctx, name: str):
        """
        Delete a product from the database.

        User story: As an admin, I delete a product.

        :raise ProductNotFound
        """
        self.product_repository.delete_product(ctx, name=name)

        # TODO: LOG.info

