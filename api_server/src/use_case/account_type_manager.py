# coding=utf-8
""" Use cases (business rule layer) of everything related to transactions. """
from dataclasses import dataclass
from typing import List

from src.entity.account_type import AccountType
from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.exceptions import IntMustBePositive, MissingRequiredField, StringMustNotBeEmpty, AccountTypeNotFoundError
from src.util.context import log_extra
from src.util.log import LOG
from src.use_case.interface.account_type_repository import AccountTypeRepository
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


class AccountTypeManager:
    def __init__(self, account_type_repository: AccountTypeRepository):
        self.account_type_repository = account_type_repository

    def get_by_id(self, ctx, account_type_id=None) -> AccountType:
        """
             Search an account_type in the database.
        """
        result, _ = self.account_type_repository.search_account_type_by(ctx, account_type_id=account_type_id)
        if not result:
            raise AccountTypeNotFoundError(account_type_id)

        # Log action.
        LOG.info('account_type_get_by_id', extra=log_extra(
            ctx,
            account_type_id=account_type_id
        ))
        return result[0]

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
               account_type_id=None, terms=None) -> (List[AccountType], int):
        """
        search account_type in the database.

        A une utilité ??

        :raise IntMustBePositiveException
        """

        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.account_type_repository.search_account_type_by(ctx,
                                                                            account_type_id=account_type_id,
                                                                            terms=terms)

        # Log action.
        LOG.info('account_type_search', extra=log_extra(ctx, account_type_id=account_type_id, terms=terms))
        return result, count
