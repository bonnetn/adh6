# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account import Account
from src.entity.account import AccountType
from src.use_case.interface.account_repository import AccountRepository


class AccountTypeSQLRepository(AccountTypeRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_account_type(self, ctx, name=None) -> None:
        """
        Create an account_type.
        Possibly raise nothing ?

        s = ctx.get(CTX_SQL_SESSION)

        # TODO: LOG.debug

        account = AccountType(
                name=name,
             
        """
        pass

        # TODO: voir si track_modifications prendre en compte account et si s.add(account) fonctionne
    
    # TODO: update_account mais même problème qu'au dessus

    def search_account_type_by(self, ctx, limit=None, offset=None, name=None, terms=None) -> (List[AccountType], int):
        """
        Search for an account_type.
        """
        pass

    def update_account_type(self, ctx, name=None,):
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        pass

        def delete_account_type(self, ctx, name=None):
        """
        Delete a acccount_type.

        :raise AccoundtNotFound (one day)
        """
        pass

def _map_account_sql_to_entity(a) -> AccountType:
    """
    Map a Account object from SQLAlchemy to a AccountType (from the entity folder/layer).
    """
    return AccountType(
        name=a.name,
     
    )
