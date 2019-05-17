from typing import List, Optional

from src.entity.account import Account
from src.entity.account_type import AccountType
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.account_repository import AccountRepository

from src.exceptions import MemberNotFoundError, IntMustBePositive

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET

# TODO: class MutationRequest(Account) pour modifier un compte et lever les différentes erreurs ?
# TODO: update_or_create


class AccountManager:
    def __init__(self, member_repository: MemberRepository, account_repository: AccountRepository):
        self.account_repository = account_repository
        self.member_repository = member_repository

    def get_by_name(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, name=None, terms=None) -> (List[Account], int):
        """
        Search an account in the database.
        """
        if limit < 0:
            raise IntMustBePositive('limit')
        if offset < 0:
            raise IntMustBePositive('limit')

        result, count = self.account_repository.search_account_by(ctx, limit=limit, offset=offset, name=name, terms=terms)
        
        # TODO: LOG.info

        return result, count

    # TODO: get_by_type and get_by_status (actif or not)
'''
Necessite la classe MutationRequest
    def update_or_create(self, ctx, name: str, actif: bool, type: AccountType, creation_date: str, req : MutationRequest):
        req.validate()
        owner, _ = self.member_repository.search_member_by(ctx, name=req.owner_username)
        
        # Pour créer un compte, il faut un membre (même pour Soirée MiNET 2018)
        
        if not owner:
            raise MemberNotFoundError(req.owner_username)

        result, _ = self.account_repository_search_account_by(ctx, name=name)
        if not result:
            # No account with that name, creating one...
            self.account_repository.create_account(ctx, name=name, type=type, actif=actif, creation_date=creation_date)
            # TODO: LOG.info
            return True

        else:
            # An account exists, updating it
            # Warning: AccountNotFound
            self.account_repository.update_account(ctx, name=name, type=type, actif=actif, creation_date=creation_date)
            # TODO: LOG.info
            return False
'''