# coding=utf-8
"""
Account repository.
"""
import abc  # pour définir des classes abstraites en python
from typing import List

from src.entity.account_type import AccountType
from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT


class AccountTypeRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle accounts.
    """

    @abc.abstractmethod
    def search_account_type_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                               account_type_id: int = None, terms: str = None) -> (List[AccountType], int):
        """
        Search for an account type.
        """
        pass
    
    @abc.abstractmethod
    def create_account_type(self, ctx, name=None):
        """
        Create an account.
        Will raise (one day) AccountAlreadyExist
        """
        pass

    @abc.abstractmethod 
    def update_account_type(self, ctx, name=None):
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        pass

    @abc.abstractmethod
    def delete_account_type(self, ctx, name) -> None:
        """
        Delete a room.
        """
        pass
