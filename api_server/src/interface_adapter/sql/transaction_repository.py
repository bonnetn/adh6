# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.transaction import Transaction
from src.interface_adapter.sql.model.models import Transaction as SQLTransaction
from src.use_case.interface.transaction_repository import TransactionRepository
from src.util.context import log_extra
from src.util.log import LOG


class TreasurySQLRepository(TransactionRepository):

    def search_transaction_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None) \
            -> (List[Transaction], int):
        LOG.debug("sql_transaction_repository_search_called", extra=log_extra(ctx))
        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SQLTransaction)

        if terms:
            q = q.filter(
                (SQLTransaction.name.contains(terms)) |
                (SQLTransaction.src_account.name.contains(terms)) |
                (SQLTransaction.dst_account.name.contains(terms))
            )

        count = q.count()
        q = q.order_by(SQLTransaction.timestamp.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_transaction_sql_to_entity, r)), count

    def create_transaction(self, ctx, src_account=None, dst_account=None, name=None, value=None, attachments=None):
        LOG.debug("sql_device_repository_create_transaction_called", extra=log_extra(ctx, name=name))
        s = ctx.get(CTX_SQL_SESSION)
        pass

    def update_transaction(self, ctx, transaction_to_update, attachments=None):
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_device_repository_update_device_called", extra=log_extra(ctx, transaction=transaction_to_update))
        pass


def _map_transaction_sql_to_entity(t: SQLTransaction) -> Transaction:
    """
    Map a Transaction object from SQLAlchemy to a Transaction (from the entity folder/layer).
    """
    return Transaction(
        src=t.src,
        dst=t.dst,
        timestamp=t.timestamp,
        name=t.name,
        value=t.value,
        type=t.payment_method
    )
