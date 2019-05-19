# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.use_case.interface.payment_method_repository import PaymentMethodRepository
from src.entity.payment_method import PaymentMethod
from typing import List


class PaymentMethodSQLRepository(PaymentMethodRepository):
    def search_payment_method_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                                 name: str = None) -> (List[PaymentMethod], int):
        pass
