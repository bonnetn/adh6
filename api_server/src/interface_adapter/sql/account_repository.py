# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account import Account
from src.interface_adapter.sql.model.models import Account as SQLAccount
from src.entity.account import AccountType
from src.use_case.interface.account_repository import AccountRepository
from src.util.context import log_extra
from src.util.log import LOG


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

    def search_account_by(self, ctx, limit=None, offset=None, account_id=None, terms=None) -> (List[Account], int):
        """
        Search for an account.
        """
        LOG.debug("sql_account_repository_search_called", extra=log_extra(ctx, account_id=account_id, terms=terms))
        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SQLAccount)

        if account_id:
            q = q.filter(SQLAccount.id == account_id)
        if terms:
            q = q.filter(SQLAccount.name.contains(terms))

        count = q.count()
        q = q.order_by(SQLAccount.creation_date.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_account_sql_to_entity, r)), count

    def update_account(self, ctx, name=None, type=None, actif=None, creation_date=None, account_id=None):
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
