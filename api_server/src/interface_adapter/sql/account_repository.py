# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from datetime import datetime
from typing import List

from src.constants import CTX_SQL_SESSION
from src.entity.account import Account
from src.exceptions import AccountNotFoundError
from src.interface_adapter.sql.model.models import Account as SQLAccount
from src.interface_adapter.sql.track_modifications import track_modifications
from src.use_case.interface.account_repository import AccountRepository
from src.util.context import log_extra
from src.util.log import LOG


class AccountSQLRepository(AccountRepository):
    """
    Represent the interface to the SQL database.
    """

    def create_account(self, ctx, name=None, actif=None, type=None, creation_date=None):
        """
        Create an account.

        :raise AccountTypeNotFound ?
        """

        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_account_repository_create_account_called", extra=log_extra(ctx, name=name, type=type))

        now = datetime.now()

        account = SQLAccount(
            name=name,
            actif=actif,
            type=type,
            creation_date=now,
        )

        with track_modifications(ctx, s, account):
            s.add(account)

        return account

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

    def update_account(self, ctx, name=None, type=None, actif=None, creation_date=None,
                       account_id=None) -> None:
        """
        Update an account.
        Will raise (one day) AccountNotFound
        """
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_account_repository_update_account_called", extra=log_extra(ctx, account_id=account_id,
                                                                                  actif=actif))

        account = _get_account_by_id(s, account_id)
        if account is None:
            raise AccountNotFoundError(account_id)

        with track_modifications(ctx, s, account):
            account.name = name or account.name
            account.type = type or account.type
            account.actif = actif
            account.creation_date = creation_date or account.creation_date


def _map_account_sql_to_entity(a) -> Account:
    """
    Map a Account object from SQLAlchemy to a Account (from the entity folder/layer).
    """
    return Account(
        name=a.name,
        actif=a.actif,
        type=a.type,
        creation_date=a.creation_date,
        account_id=a.id
    )


def _get_account_by_id(s, id) -> SQLAccount:
    return s.query(SQLAccount).filter(SQLAccount.id == id).one_or_none()
