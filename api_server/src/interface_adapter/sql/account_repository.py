# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account import Account
from src.use_case.interface.account_repository import AccountRepository

class AccountSQLRepository(AccountRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_account(self, ctx, name=None, actif=None, type=None, creation_date=None) -> None:
        """
        Create an account.
        Possibly raise nothing ?
        """
        s = ctx.get(CTX_SQL_SESSION)

        #TODO: LOG.debug

        account = Account(
                name=name,
                actif=actif,
                type=type,
                creation_date=creation_date)

        #TODO: voir si track_modifications prendre en compte account et si s.add(account) fonctionne
    
   #TODO: update_account mais même problème qu'au dessus


