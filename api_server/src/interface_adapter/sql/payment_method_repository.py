# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET, CTX_SQL_SESSION
from src.use_case.interface.payment_method_repository import PaymentMethodRepository
from src.entity.payment_method import PaymentMethod
from typing import List
from src.interface_adapter.sql.model.models import PaymentMethod as SQLPaymentMethod

from src.util.context import log_extra
from src.util.log import LOG


class PaymentMethodSQLRepository(PaymentMethodRepository):
    def search_payment_method_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                                 payment_method_id=None, terms: str = None) -> (List[PaymentMethod], int):
        LOG.debug("sql_payment_method_repository_search_called", extra=log_extra(ctx))
        s = ctx.get(CTX_SQL_SESSION)

        q = s.query(SQLPaymentMethod)

        if payment_method_id:
            q = q.filter(SQLPaymentMethod.id == payment_method_id)
        if terms:
            q = q.filter(SQLPaymentMethod.name.contains(terms))

        count = q.count()
        q = q.order_by(SQLPaymentMethod.id.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(_map_account_sql_to_entity, r)), count


def _map_account_sql_to_entity(a) -> PaymentMethod:
    """
    Map a Account object from SQLAlchemy to a Account (from the entity folder/layer).
    """

    return PaymentMethod(
        payment_method_id=a.id,
        name=a.name
    )
