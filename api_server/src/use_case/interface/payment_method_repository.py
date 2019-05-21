# coding=utf-8
"""
Payment method repository.
"""
import abc
from typing import List

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.entity.payment_method import PaymentMethod


class PaymentMethodRepository:
    """
    Abstract interface to handle payment methods.
    """

    @abc.abstractmethod
    def search_payment_method_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                                 name: str = None, terms: str = None) -> (List[PaymentMethod], int):
        """
        Search payment methods.
        """
        pass
