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
class AccountTypeRequest:
    """
    Mutation request for a transaction. This represents the 'diff' that is going to be applied on a transaction object.

    If a field is set to None, field be left untouched.
    """

    name : varchar(255)
 
    def validate(self):
          """
          TODO   
          """
        pass


class AccountTypeManager:

    def __init__(self,
                 account_type_repository: AccountTypeRepository,
                 ):
        self.account_type_repository = account_type_repository

    def get_by_name(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, name=None) -> (List[AccountType], int):
        """
             Search an account_type in the database.

        """
        result, count = self.account_type_repository.search_account_type_by(ctx, name=name)
        if not result:
            raise AccountTypeNotFoundError(name)

        # Log action.
        LOG.info('account_type_get_by_name', extra=log_extra(
            ctx,
            name='name'
        ))
        return result[0], count


    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, name=None) -> (List[AccountType], int):
        """
        search transactionsaccount_type in the database.

        A une utilité ??

        :raise IntMustBePositiveException
        """

        result, count = self.account_type_repository.search_transaction_by(ctx,
                                                                          limit=limit,
                                                                          offset=offset,
                                                                          terms=terms)

        # Log action.
        LOG.info('transaction_search', extra=log_extra(
            ctx,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, account_type_request: AccountTypeRequest) -> bool:
        """
        Create/Update an account_type from the database.

        :return: True if the account_type was created, false otherwise.


        Pour créer un compteaccount_ype, il faut un account
        """
        # Make sure all the field objects set are valid.
        mutation_request.validate()

         account, _ = self.account_repository.search_account_by(ctx, name=req.account_name)

         if not account:
            raise AccountNotFoundError(req.owner_name)


     result, _ = self.account_type_repository_search_account_type_by(ctx, name=name)
        if not result:
            # No account_type with that name, creating one...
            self.account_type_repository.create_account_type(ctx, name=name)
            # TODO: LOG.info
            return True

        else:
            # An account exists, updating it
            # Warning: AccountTypeNotFound
            self.account_type_repository.update_account_type(ctx, name=name)
            # TODO: LOG.info
            return False
