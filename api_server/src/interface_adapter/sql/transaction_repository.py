# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from datetime import datetime
from typing import List

from sqlalchemy.orm import aliased

from src.constants import CTX_SQL_SESSION, DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.transaction import Transaction
from src.exceptions import AccountNotFoundError, PaymentMethodNotFoundError
from src.interface_adapter.sql.account_repository import _map_account_sql_to_entity
from src.interface_adapter.sql.model.models import Transaction as SQLTransaction, Account, PaymentMethod
from src.interface_adapter.sql.payment_method_repository import _map_payment_method_sql_to_entity
from src.interface_adapter.sql.track_modifications import track_modifications
from src.use_case.interface.transaction_repository import TransactionRepository
from src.util.context import log_extra
from src.util.log import LOG


class TransactionSQLRepository(TransactionRepository):

    def search_transaction_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, transaction_id=None,
                              account_id=None, terms=None) \
            -> (List[Transaction], int):
        LOG.debug("sql_transaction_repository_search_called", extra=log_extra(ctx))
        s = ctx.get(CTX_SQL_SESSION)

        account_source = aliased(Account)
        account_destination = aliased(Account)

        q = s.query(SQLTransaction)
        q = q.join(account_source, account_source.id == SQLTransaction.dst)
        q = q.join(account_destination, account_destination.id == SQLTransaction.src)

        if transaction_id:
            q = q.filter(SQLTransaction.id == transaction_id)
        if terms:
            q = q.filter(
                (SQLTransaction.name.contains(terms))
            )
        if account_id:
            q = q.filter(
                (SQLTransaction.src == account_id) |
                (SQLTransaction.dst == account_id)
            )

        count = q.count()
        q = q.order_by(SQLTransaction.timestamp.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_transaction_sql_to_entity, r)), count

    def create_transaction(self, ctx, src=None, dst=None, name=None, value=None, payment_method=None, attachments=None):
        LOG.debug("sql_device_repository_create_transaction_called", extra=log_extra(ctx, name=name))
        """
        Create a transaction.

        :raise AccountNotFound
        """
        s = ctx.get(CTX_SQL_SESSION)
        LOG.debug("sql_transaction_repository_create_transaction_called", extra=log_extra(ctx, name=name))

        now = datetime.now()

        account_src = None
        if src is not None:
            account_src = s.query(Account).filter(Account.id == src).one_or_none()
            if not account_src:
                raise AccountNotFoundError(src)

        account_dst = None
        if dst is not None:
            account_dst = s.query(Account).filter(Account.id == dst).one_or_none()
            if not account_dst:
                raise AccountNotFoundError(dst)

        method = None
        if payment_method is not None:
            method = s.query(PaymentMethod).filter(PaymentMethod.id == payment_method).one_or_none()
            if not method:
                raise PaymentMethodNotFoundError(payment_method)

        transaction = SQLTransaction(
            src_account=account_src,
            dst_account=account_dst,
            value=value,
            name=name,
            timestamp=now,
            attachments="",
            payment_method=method
        )

        with track_modifications(ctx, s, transaction):
            s.add(transaction)
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
        src=_map_account_sql_to_entity(t.src_account),
        dst=_map_account_sql_to_entity(t.dst_account),
        timestamp=t.timestamp,
        name=t.name,
        value=t.value,
        payment_method=_map_payment_method_sql_to_entity(t.payment_method),
        attachments=t.attachments
    )
