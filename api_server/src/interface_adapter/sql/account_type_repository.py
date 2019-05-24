# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.entity.account_type import AccountType
from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.interface_adapter.sql.model.models import AccountType as SQLAccountType
from src.use_case.interface.account_type_repository import AccountTypeRepository
from src.util.context import log_extra
from src.util.log import LOG


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

    def search_account_type_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                               account_type_id=None, terms: str = None) -> (List[AccountType], int):
        LOG.debug("sql_payment_method_repository_search_called", extra=log_extra(ctx))
        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SQLAccountType)

        if account_type_id:
            q = q.filter(SQLAccountType.id == account_type_id)
        if terms:
            q = q.filter(SQLAccountType.name.contains(terms))

        count = q.count()
        q = q.order_by(SQLAccountType.id.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_account_sql_to_entity, r)), count

    def update_account_type(self, ctx, name=None, ):
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
        account_type_id=a.id,
        name=a.name,
    )
