# coding=utf-8
from dataclasses import dataclass
from typing import List

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.payment_method import PaymentMethod
from src.exceptions import MissingRequiredField, StringMustNotBeEmpty, IntMustBePositive, PaymentMethodNotFoundError
from src.use_case.interface.payment_method_repository import PaymentMethodRepository
from src.util.context import log_extra
from src.util.log import LOG
from src.util.validator import is_empty


@dataclass
class MutationRequest:
    """
     Mutation request for a payment method. This represents the 'diff',
     that is going to be applied on the payment method object.
     """

    name: str

    def validate(self):
        """
        Validate the fields that are set in a MutationRequest.
        """
        if self.name is None:
            raise MissingRequiredField('name')

        if is_empty(self.name):
            raise StringMustNotBeEmpty('name')


class PaymentMethodManager:
    def __init__(self, payment_method_repository: PaymentMethodRepository):
        self.payment_method_repository = payment_method_repository

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, payment_method_id=None,
               terms=None) -> (List[PaymentMethod], int):
        """
        Search payment methods in the database.
        """

        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.payment_method_repository.search_payment_method_by(ctx, limit=limit,
                                                                                offset=offset,
                                                                                payment_method_id=payment_method_id,
                                                                                terms=terms)
        LOG.info("payment_method_search",
                 extra=log_extra(ctx, payment_method_id=payment_method_id, terms=terms))

        return result, count

    def get_by_id(self, ctx, payment_method_id=None) -> PaymentMethod:
        """
        Retrieves a payment method given its name.
        """
        result, _ = self.payment_method_repository.search_payment_method_by(ctx, payment_method_id=payment_method_id)
        LOG.info('payment_method_get_by_id', extra=log_extra(ctx, payment_method_id=payment_method_id))

        if not result:
            raise PaymentMethodNotFoundError(payment_method_id)

        return result[0]
