# coding=utf-8
"""
Product repository.
"""
import abc
from typing import List

from src.entity.product import Product


class ProductRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle product.
    """

    @abc.abstractmethod
    def search_product_by(self, ctx, limit=None, offset=None, name=None, terms=None) -> \
            (List[Product], int):
        """
        Search for a product.
        """
        pass

    @abc.abstractmethod
    def create_product(self, ctx, name=None, buying_price=None, selling_price=None):
        """
        Create a product.

        :raise ProductAlreadyExist (one day)
        """
        pass

    @abc.abstractmethod
    def update_product(self, ctx, product_to_update, name=None, buying_price=None, selling_price=None):
        """
        Update a product.

        :raise ProductNotFound (one day)
        """
        pass

    @abc.abstractmethod
    def delete_product(self, ctx, name=None):
        """
        Delete a product.

        :raise ProductNotFound (one day)
        """
        pass
