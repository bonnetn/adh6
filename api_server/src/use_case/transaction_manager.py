# coding=utf-8
""" Use cases (business rule layer) of everything related to transactions. """
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.entity.member import Member
from src.exceptions import InvalidAdmin, MemberNotFoundError, IntMustBePositive, MissingRequiredField, \
    PaymentMethodNotFoundError
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
    type: Optional[str] = None
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
    type: str

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
        if self.type is None:
            raise MissingRequiredField('type')

        super().validate()


class TransactionManager:
    """
    Implements all the use cases related to transaction management.
    """

    def __init__(self,
                 transaction_repository: TransactionRepository,
                 ):
        self.transaction_repository = transaction_repository

    def get_by_username(self, ctx, username) -> Member:
        """
        User story: As an admin, I can see the profile of a member, so that I can help her/him.

        :raise MemberNotFound
        """
        result, _ = self.transaction_repository.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFoundError(username)

        # Log action.
        LOG.info('member_get_by_username', extra=log_extra(
            ctx,
            username='username'
        ))
        return result[0]

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None) -> (
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
                                                                          terms=terms)

        # Log action.
        LOG.info('transaction_search', extra=log_extra(
            ctx,
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
