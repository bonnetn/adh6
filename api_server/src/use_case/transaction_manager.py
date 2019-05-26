# coding=utf-8
""" Use cases (business rule layer) of everything related to transactions. """
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.exceptions import IntMustBePositive, MissingRequiredField, \
    TransactionNotFoundError, UserInputError
from src.interface_adapter.sql.model.models import Transaction
from src.use_case.interface.transaction_repository import TransactionRepository
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class PartialMutationRequest:
    """
    Mutation request for a transaction. This represents the 'diff' that is going to be applied on a transaction object.

    If a field is set to None, field be left untouched.
    """
    src: Optional[str] = None
    dst: Optional[str] = None
    name: Optional[str] = None
    value: Optional[int] = None
    paymentMethod: Optional[str] = None
    attachments: Optional[str] = None

    def validate(self):
        pass


@dataclass
class FullMutationRequest(PartialMutationRequest):
    """
    Mutation request for a transaction. This represents the 'diff' that is going to be applied on a transaction object.

    If a field is set to None, field be left untouched.
    """
    src: str
    dst: str
    name: str
    value: int
    paymentMethod: str
    attachments: Optional[str] = None

    def validate(self):
        # SOURCE:
        if self.src is None:
            raise MissingRequiredField('src')

        # DESTINATION:
        if self.dst is None:
            raise MissingRequiredField('dst')

        # NAME:
        if self.name is None:
            raise MissingRequiredField('name')

        # VALUE:
        if self.value is None:
            raise MissingRequiredField('value')

        # TYPE:
        if self.paymentMethod is None:
            raise MissingRequiredField('paymentMethod')

        super().validate()


class TransactionManager:
    """
    Implements all the use cases related to transaction management.
    """

    def __init__(self,
                 transaction_repository: TransactionRepository,
                 ):
        self.transaction_repository = transaction_repository

    def get_by_id(self, ctx, transaction_id) -> Transaction:
        """
        User story: As an admin, I can see the details of a transaction.

        :raise TransactionNotFound
        """
        result, _ = self.transaction_repository.search_transaction_by(ctx, transaction_id=transaction_id)
        if not result:
            raise TransactionNotFoundError(transaction_id)

        # Log action.
        LOG.info('transaction_get_by_id', extra=log_extra(
            ctx,
            transaction_id=transaction_id
        ))
        return result[0]

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, account_id=None, terms=None) -> (
            List[Transaction], int):
        """
        search transactions in the database.

        :raise IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.transaction_repository.search_transaction_by(ctx,
                                                                          limit=limit,
                                                                          offset=offset,
                                                                          account_id=account_id,
                                                                          terms=terms)

        # Log action.
        LOG.info('transaction_search', extra=log_extra(
            ctx,
            account_id=account_id,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, mutation_request: FullMutationRequest) -> bool:
        """
        Create/Update a transaction from the database.

        :return: True if the transaction was created, false otherwise.

        :raise IntMustBePositiveException
        :raise AccountNotFound
        :raise InvalidAdmin
        :raise PaymentMethodNotFound
        :raise MissingRequiredFieldError
        """
        # Make sure all the field objects set are valid.
        mutation_request.validate()

        if mutation_request.value < 0:
            raise IntMustBePositive('value')
        if mutation_request.src == mutation_request.dst:
            raise UserInputError('source and destination accounts must not be the same')

        # Build a dict that will be transformed into a transaction. If a field is not set, consider that it should be
        # None.

        fields = asdict(mutation_request)
        fields = {k: v for k, v in fields.items()}

        try:
            self.transaction_repository.create_transaction(ctx, **fields)
        except Exception:
            raise

        # Log action
        LOG.info('transaction_create', extra=log_extra(
            ctx,
            mutation=json.dumps(fields, sort_keys=True, default=str)
        ))

        return True

    def update_partially(self, ctx, mutation_request: PartialMutationRequest) -> None:
        pass
