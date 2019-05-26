# coding=utf-8
"""
Treasury repository.
"""
import abc
from typing import List

from src.entity.transaction import Transaction


class TransactionRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle devices.
    """

    @abc.abstractmethod
    def search_transaction_by(self, ctx, limit=None, offset=None, account_id=None, transaction_id=None, terms=None) -> \
            (List[Transaction], int):
        """
        Search for a transaction.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_transaction(self, ctx, src=None, dst=None, name=None, value=None, paymentMethod=None, attachments=None):
        """
        Create a transaction.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_transaction(self, ctx, transaction_to_update, attachments=None):
        """
        Update a transaction to add an invoice.

        :raise TransactionNotFound
        """
        pass  # pragma: no cover
