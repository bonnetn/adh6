# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account import Account
from src.entity.account import AccountType
from src.use_case.interface.account_repository import AccountRepository


class AccountSQLRepository(AccountRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_account(self, ctx, name=None, actif=None, type=None, creation_date=None) -> None:
        """
        Create an account.
        Possibly raise nothing ?

        s = ctx.get(CTX_SQL_SESSION)

        # TODO: LOG.debug

        account = Account(
                name=name,
                actif=actif,
                type=type,
                creation_date=creation_date)
        """
        pass

        # TODO: voir si track_modifications prendre en compte account et si s.add(account) fonctionne
    
    # TODO: update_account mais même problème qu'au dessus

    def search_account_by(self, ctx, limit=None, offset=None, name=None, terms=None) -> (List[Account], int):
        """
        Search for an account.
        """
        pass

    def update_account(self, ctx, name=None, type=None, actif=None, creation_date=None):
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        pass


def _map_account_sql_to_entity(a) -> Account:
    """
    Map a Account object from SQLAlchemy to a Account (from the entity folder/layer).
    """
    t = AccountType.Adherent
    if a.type == 'club':
        t = AccountType.Club
    if a.type == 'event':
        t = AccountType.Event
    return Account(
        name=a.name,
        actif=a.actif,
        type=t,
        creation_date=a.creation_date,
    )
