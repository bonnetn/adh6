# coding=utf-8
"""
Account repository.
"""
import abc  # pour définir des classes abstraites en python
from typing import List
from src.entity.account import Account


class AccountRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle accounts.
    """

    @abc.abstractmethod
    def search_account_by(self, ctx, limit=None, offset=None, account_id=None, terms=None) -> (List[Account], int):
        """
        Search for an account.
        """
        pass
    
    @abc.abstractmethod
    def create_account(self, ctx, name=None, type=None, actif=None, creation_date=None):
        """
        Create an account.
        Will raise (one day) AccountAlreadyExist
        """
        pass

    @abc.abstractmethod 
    def update_account(self, ctx, account_id=None, name=None, type=None, actif=None, creation_date=None):
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        pass
