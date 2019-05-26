from pytest import fixture, raises
from unittest.mock import MagicMock

from pytest import fixture, raises

from src.entity.transaction import Transaction
from src.exceptions import TransactionNotFoundError, IntMustBePositive, UserInputError
from src.use_case.interface.transaction_repository import TransactionRepository
from src.use_case.transaction_manager import TransactionManager, FullMutationRequest

TEST_TRANSACTION_ID = '1'


class TestGetByID:
    def test_happy_path(self,
                        ctx,
                        mock_transaction_repository: TransactionRepository,
                        sample_transaction: Transaction,
                        transaction_manager: TransactionManager):
        mock_transaction_repository.search_transaction_by = MagicMock(return_value=([sample_transaction], 1))
        result = transaction_manager.get_by_id(ctx, TEST_TRANSACTION_ID)

        assert sample_transaction == result
        mock_transaction_repository.search_transaction_by.assert_called_once()

    def test_transaction_not_found(self,
                                   ctx,
                                   mock_transaction_repository: TransactionRepository,
                                   transaction_manager: TransactionManager):
        mock_transaction_repository.search_transaction_by = MagicMock(return_value=([], 0))

        with raises(TransactionNotFoundError):
            transaction_manager.get_by_id(ctx, TEST_TRANSACTION_ID)


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_transaction_repository: TransactionRepository,
                        sample_transaction: Transaction,
                        transaction_manager: TransactionManager):
        mock_transaction_repository.search_transaction_by = MagicMock(return_value=([sample_transaction], 1))
        result, count = transaction_manager.search(ctx, limit=42, offset=2, terms='abc')

        assert [sample_transaction] == result
        assert 1 == count
        mock_transaction_repository.search_transaction_by.assert_called_once_with(ctx, account_id=None, limit=42,
                                                                                  offset=2, terms='abc')

    def test_offset_negative(self,
                             ctx,
                             transaction_manager: TransactionManager):
        with raises(IntMustBePositive):
            transaction_manager.search(ctx, offset=-1)

    def test_limit_negative(self,
                            ctx,
                            transaction_manager: TransactionManager):
        with raises(IntMustBePositive):
            transaction_manager.search(ctx, limit=-1)


"""
class TestUpdate:
    def test_happy_path(self,
                        ctx,
                        mock_transaction_repository: TransactionRepository,
                        transaction_manager: TransactionManager):
        req = FullMutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        mock_transaction_repository.update_switch = MagicMock()

        transaction_manager.update(ctx, '2', req)

        mock_transaction_repository.update_switch.assert_called_once_with(ctx, switch_id='2', **asdict(req))

    def test_switch_not_found(self,
                              ctx,
                              mock_transaction_repository: TransactionRepository,
                              transaction_manager: TransactionManager):
        req = FullMutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        mock_transaction_repository.update_switch = MagicMock(side_effect=TransactionNotFoundError)

        with raises(TransactionNotFoundError):
            transaction_manager.update(ctx, '2', req)

    def test_missing_required_field(self,
                                    ctx,
                                    mock_transaction_repository: TransactionRepository,
                                    transaction_manager: TransactionManager):
        req = FullMutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        req.community = None
        mock_transaction_repository.update_switch = MagicMock()

        with raises(MissingRequiredField):
            transaction_manager.update(ctx, '2', req)

        mock_transaction_repository.update_switch.assert_not_called()

    @mark.parametrize('field,value', [
        ('ip_v4', None),
        ('ip_v4', 'not an ipv4 address'),
        ('description', None),
        ('community', None),
    ])
    def test_invalid_mutation_request(self,
                                      ctx,
                                      mock_transaction_repository: TransactionRepository,
                                      field: str,
                                      value,
                                      transaction_manager: TransactionManager):
        req = FullMutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        req = FullMutationRequest(**{**asdict(req), **{field: value}})
        mock_transaction_repository.update_switch = MagicMock()

        with raises(ValueError):
            transaction_manager.update(ctx, '2', req)"""


class TestCreate:
    def test_happy_path(self,
                        ctx, mock_transaction_repository: TransactionRepository,
                        transaction_manager: TransactionManager):
        req = FullMutationRequest(
            src='1',
            dst='2',
            name='test',
            value=1,
            paymentMethod='1',
            attachments=None

        )
        mock_transaction_repository.create_transaction = MagicMock()

        transaction_manager.update_or_create(ctx, req)

        mock_transaction_repository.create_transaction.assert_called_once_with(ctx, src=req.src, dst=req.dst,
                                                                               name=req.name, value=req.value,
                                                                               paymentMethod=req.paymentMethod,
                                                                               attachments=None)

    def test_same_account(self,
                          ctx,
                          transaction_manager: TransactionManager):
        req = FullMutationRequest(
            src='1',
            dst='1',
            name='test',
            value=1,
            paymentMethod='1',
            attachments=None

        )
        with raises(UserInputError):
            transaction_manager.update_or_create(ctx, req)


@fixture
def transaction_manager(mock_transaction_repository, ):
    return TransactionManager(
        transaction_repository=mock_transaction_repository
    )


@fixture
def mock_transaction_repository():
    return MagicMock(spec=TransactionRepository)
