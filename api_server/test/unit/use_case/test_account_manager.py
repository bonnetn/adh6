from dataclasses import asdict
from unittest.mock import MagicMock

from pytest import fixture, raises, mark

from src.entity.account import Account
from src.exceptions import AccountNotFoundError, MissingRequiredField, IntMustBePositive
from src.use_case.account_manager import AccountManager, FullMutationRequest
from src.use_case.interface.account_repository import AccountRepository
from src.use_case.interface.member_repository import MemberRepository

TEST_ACCOUNT_ID = 1200


class TestGetByID:
    def test_happy_path(self,
                        ctx,
                        mock_account_repository: AccountRepository,
                        sample_account: Account,
                        account_manager: AccountManager):
        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        result = account_manager.get_by_id(ctx, account_id=TEST_ACCOUNT_ID)

        assert sample_account == result
        mock_account_repository.search_account_by.assert_called_once()

    def test_account_not_found(self,
                               ctx,
                               mock_account_repository: AccountRepository,
                               account_manager: AccountManager):
        mock_account_repository.search_account_by = MagicMock(return_value=([], 0))

        with raises(AccountNotFoundError):
            account_manager.get_by_id(ctx, account_id=TEST_ACCOUNT_ID)


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_account_repository: AccountRepository,
                        sample_account: Account,
                        account_manager: AccountManager):
        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        result, count = account_manager.search(ctx, limit=42, offset=2, account_id=None, terms='abc')

        assert [sample_account] == result
        assert 1 == count
        mock_account_repository.search_account_by.assert_called_once_with(ctx, limit=42, offset=2, account_id=None,
                                                                          terms='abc')

    def test_offset_negative(self,
                             ctx,
                             account_manager: AccountManager):
        with raises(IntMustBePositive):
            account_manager.search(ctx, limit=42, offset=-1, account_id=None, terms=None)

    def test_limit_negative(self,
                            ctx,
                            account_manager: AccountManager):
        with raises(IntMustBePositive):
            account_manager.search(ctx, limit=-1, offset=2, account_id=None, terms=None)


class TestUpdate:
    def test_happy_path(self,
                        ctx,
                        mock_account_repository: AccountRepository,
                        sample_account: Account,
                        account_manager: AccountManager):
        req = FullMutationRequest(
            name='MiNET',
            type=1,
            actif=True,
            creation_date='21/05/2019',
        )
        mock_account_repository.update_account = MagicMock()

        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        account_manager.update_or_create(ctx, req, account_id=1)

        mock_account_repository.update_account.assert_called_once_with(ctx, **asdict(req), account_id=1)

    def test_account_not_found(self,
                               ctx,
                               mock_account_repository: AccountRepository,
                               sample_account: Account,
                               account_manager: AccountManager):
        req = FullMutationRequest(
            name='MiNET',
            type=1,
            actif=True,
            creation_date='21/05/2019',
        )
        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        mock_account_repository.update_account = MagicMock(side_effect=AccountNotFoundError)

        with raises(AccountNotFoundError):
            account_manager.update_or_create(ctx, req, TEST_ACCOUNT_ID)

        mock_account_repository.search_account_by.assert_called_once_with(ctx, account_id=TEST_ACCOUNT_ID)

    def test_missing_required_field(self,
                                    ctx,
                                    mock_account_repository: AccountRepository,
                                    sample_account: Account,
                                    account_manager: AccountManager):
        req = FullMutationRequest(
            name=None,
            type=1,
            actif=True,
            creation_date='21/05/2019',
        )
        req.community = None
        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        mock_account_repository.update_account = MagicMock()

        with raises(MissingRequiredField):
            account_manager.update_or_create(ctx, req, account_id=None)

        mock_account_repository.update_account.assert_not_called()

    @mark.parametrize('field,value', [
        ('name', None),
        ('actif', True),
        ('type', None),
        ('creation_date', None),
    ])
    def test_invalid_mutation_request(self,
                                      ctx,
                                      mock_account_repository: AccountRepository,
                                      sample_account: Account,
                                      field: str,
                                      value,
                                      account_manager: AccountManager):
        req = FullMutationRequest(
            name='',
            type=1,
            actif=True,
            creation_date='21/05/2019',
        )
        req = FullMutationRequest(**{**asdict(req), **{field: value}})
        mock_account_repository.search_account_by = MagicMock(return_value=([sample_account], 1))
        mock_account_repository.update_account = MagicMock()

        with raises(ValueError):
            account_manager.update_or_create(ctx, req, account_id=None)


class TestCreate:
    def test_happy_path(self,
                        ctx, mock_account_repository: AccountRepository, sample_account: Account,
                        account_manager: AccountManager):
        req = FullMutationRequest(
            name='MiNET',
            type=1,
            actif=True,
            creation_date='21/05/2019',
        )
        mock_account_repository.create_account = MagicMock()
        mock_account_repository.search_account_by = MagicMock(return_value=([], 0))
        account_manager.update_or_create(ctx, req, account_id=None)

        mock_account_repository.create_account.assert_called_once_with(ctx, name=req.name, type=req.type,
                                                                       actif=req.actif, creation_date=req.creation_date)


@fixture
def account_manager(mock_member_repository, mock_account_repository):
    return AccountManager(
        member_repository=mock_member_repository,
        account_repository=mock_account_repository
    )


@fixture
def mock_account_repository():
    return MagicMock(spec=AccountRepository)


@fixture
def mock_member_repository():
    return MagicMock(spec=MemberRepository)
