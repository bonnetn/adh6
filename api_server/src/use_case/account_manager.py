from typing import List, Optional
from dataclasses import dataclass, asdict

from src.entity.account import Account
from src.entity.account_type import AccountType
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.account_repository import AccountRepository

from src.exceptions import AccountNotFoundError, IntMustBePositive, StringMustNotBeEmpty, InvalidDate, \
    MissingRequiredField

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.util.validator import is_empty, is_date

from src.util.context import log_extra
from src.util.log import LOG

# TODO: update_or_create

@dataclass
class PartialMutationRequest:
    """
    Mutation request for an account. This represents the 'diff', that is going to be applied on the account object.

    If a field is set to None, field be left untouched.
    """
    name: str = None
    type: AccountType = None
    creation_date: Optional[str] = None
    actif: Optional[bool] = None

    def validate(self):
        # NAME:
        if self.name is not None and not is_empty(self.name):
            raise StringMustNotBeEmpty('name')

        # CREATION_DATE:
        if self.creation_date is not None and not is_date(self.creation_date):
            raise InvalidDate(self.creation_date)


@dataclass
class FullMutationRequest(PartialMutationRequest):
    """
    Mutation request for a an. This represents the 'diff', that is going to be applied on the account object.

    If a field is set to None, field will be cleared in the database.
    """
    name: str = None
    type: AccountType = None
    creation_date: Optional[str] = None
    actif: Optional[bool] = None

    def validate(self):
        # NAME:
        if self.name is None:
            raise MissingRequiredField('name')


class AccountManager:
    def __init__(self, member_repository: MemberRepository, account_repository: AccountRepository):
        self.account_repository = account_repository
        self.member_repository = member_repository

    def get_by_id(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, account_id=None, terms=None) -> (List[Account], int):
        """
        Search an account in the database.
        """
        if limit < 0:
            raise IntMustBePositive('limit')
        if offset < 0:
            raise IntMustBePositive('limit')

        result, count = self.account_repository.search_account_by(ctx, limit=limit, offset=offset, account_id=account_id, terms=terms)

        if count == 0:
            raise AccountNotFoundError
        
        # TODO: LOG.info

        return result[0]

    # TODO: get_by_type and get_by_status (actif or not)

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, account_id=None, terms=None) -> (
            List[Account], int):
        """
        search member in the database.

        user story: as an admin, i want to have a list of accounts with some filters, so that i can browse and find
        accounts.

        :raise intmustbepositiveexception
        """
        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.account_repository.search_account_by(ctx,
                                                                limit=limit,
                                                                offset=offset,
                                                                account_id=account_id,
                                                                terms=terms)

        # Log action.
        LOG.info('account_search', extra=log_extra(
            ctx,
            account_id=account_id,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, name: str, actif: bool, type: AccountType, creation_date: str,  \
                         req : FullMutationRequest,  account_id=None) -> bool:
        req.validate()
        try:
            result, _ = self.account_repository.search_account_by(ctx, limit=1, offset=0, account_id=account_id, terms=None)
        except AccountNotFoundError:
            raise
        if name == '':
            raise StringMustNotBeEmpty('name')
        if not name:
            raise MissingRequiredField('name')
        if not result:
            # No account with that name, creating one...
            self.account_repository.create_account(ctx, name=name, type=type, actif=actif, creation_date=creation_date)
            # TODO: LOG.info
            return True

        else:
            # An account exists, updating it
            # Warning: AccountNotFound
            self.account_repository.update_account(ctx, name=name, type=type, actif=actif, creation_date=creation_date,\
                                                   account_id=account_id)
            # TODO: LOG.info
            return False
