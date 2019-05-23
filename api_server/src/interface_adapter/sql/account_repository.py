# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from datetime import datetime

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.account import Account
from src.exceptions import AccountNotFoundError
from src.interface_adapter.sql.track_modifications import track_modifications
from src.interface_adapter.sql.model.models import Account as SQLAccount
from src.entity.account import AccountType
from src.use_case.interface.account_repository import AccountRepository
from src.util.context import log_extra
from src.util.log import LOG


class AccountSQLRepository(AccountRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_account(self, ctx, name=None, actif=None, type=None) -> None:
        """
        Create an account.

        :raise AccountTypeNotFound ?
        """

        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_account_repository_create_account_called", extra=log_extra(ctx, name=name))

        now = datetime.now()

        account = Account(
            name=name,
            actif=actif,
            type=type,
            creation_date=now,
        )

        with track_modifications(ctx, s, account):
            s.add(account)
        pass
    
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

    def update_account(self, ctx, account_to_update, name=None, type=None, actif=None, creation_date=None, \
                       account_id=None) -> None:
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_account_repository_update_account_called", extra=log_extra(ctx, account_id=account_to_update))

        account = _get_account_by_id(s, account_id)
        if account is None:
            raise AccountNotFoundError(account_to_update)

        with track_modifications(ctx, s, account):
            account.name = name or account.name
            account.type = type or account.type
            account.actif = actif or account.actif
            account.creation_date = creation_date or account.creation_date


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


def _get_account_by_id(s, id) -> Account:
    return s.query(Account).filter(Account.id == id).one_or_none()