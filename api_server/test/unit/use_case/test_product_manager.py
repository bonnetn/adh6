from dataclasses import asdict
from unittest.mock import MagicMock

from pytest import fixture, raises, mark

from src.entity.product import Product
from src.exceptions import ProductNotFoundError, MissingRequiredField, IntMustBePositive
from src.use_case.product_manager import ProductManager, FullMutationRequest
from src.use_case.interface.product_repository import ProductRepository

TEST_PRODUCT_ID = 1200
TEST_PRODUCT_NAME = "loutre"


class TestGetByID:
    def test_happy_path(self,
                        ctx,
                        mock_product_repository: ProductRepository,
                        sample_product: Product,
                        product_manager: ProductManager):
        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        result = product_manager.get_by_id(ctx, product_id=TEST_PRODUCT_ID)

        assert sample_product == result
        mock_product_repository.search_product_by.assert_called_once()

    def test_product_not_found(self,
                               ctx,
                               mock_product_repository: ProductRepository,
                               product_manager: ProductManager):
        mock_product_repository.search_product_by = MagicMock(return_value=([], 0))

        with raises(ProductNotFoundError):
            product_manager.get_by_id(ctx, product_id=TEST_PRODUCT_ID)


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_product_repository: ProductRepository,
                        sample_product: Product,
                        product_manager: ProductManager):
        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        result, count = product_manager.search(ctx, limit=42, offset=2, product_id=None, terms='abc')

        assert [sample_product] == result
        assert 1 == count
        mock_product_repository.search_product_by.assert_called_once_with(ctx, limit=42, offset=2, product_id=None,
                                                                          terms='abc')

    def test_offset_negative(self,
                             ctx,
                             product_manager: ProductManager):
        with raises(IntMustBePositive):
            product_manager.search(ctx, limit=42, offset=-1, product_id=None, terms=None)

    def test_limit_negative(self,
                            ctx,
                            product_manager: ProductManager):
        with raises(IntMustBePositive):
            product_manager.search(ctx, limit=-1, offset=2, product_id=None, terms=None)


class TestUpdate:
    def test_happy_path(self,
                        ctx,
                        mock_product_repository: ProductRepository,
                        sample_product: Product,
                        product_manager: ProductManager):
        req = FullMutationRequest(
            name='panthere',
            selling_price=9999,
            buying_price=999,
        )
        mock_product_repository.update_product = MagicMock()

        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        product_manager.update_or_create(ctx, req, product_id=1)

        mock_product_repository.update_product.assert_called_once_with(ctx, **asdict(req), product_id=1)

    def test_product_not_found(self,
                               ctx,
                               mock_product_repository: ProductRepository,
                               sample_product: Product,
                               product_manager: ProductManager):
        req = FullMutationRequest(
            name='MiNET',
            selling_price=9999,
            buying_price=999,
        )
        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        mock_product_repository.update_product = MagicMock(side_effect=ProductNotFoundError)

        with raises(ProductNotFoundError):
            product_manager.update_or_create(ctx, req, TEST_PRODUCT_ID)

        mock_product_repository.search_product_by.assert_called_once_with(ctx, product_id=TEST_PRODUCT_ID)

    def test_missing_required_field(self,
                                    ctx,
                                    mock_product_repository: ProductRepository,
                                    sample_product: Product,
                                    product_manager: ProductManager):
        req = FullMutationRequest(
            name=None,
            selling_price=99,
            buying_price=999,
        )
        req.community = None
        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        mock_product_repository.update_product = MagicMock()

        with raises(MissingRequiredField):
            product_manager.update_or_create(ctx, req, product_id=None)

        mock_product_repository.update_product.assert_not_called()

    @mark.parametrize('field,value', [
        ('name', None),
        ('selling_price', None),
        ('buying_price', None),
    ])
    def test_invalid_mutation_request(self,
                                      ctx,
                                      mock_product_repository: ProductRepository,
                                      sample_product: Product,
                                      field: str,
                                      value,
                                      product_manager: ProductManager):
        req = FullMutationRequest(
            name='',
            selling_price=999,
            buying_price=99,
        )
        req = FullMutationRequest(**{**asdict(req), **{field: value}})
        mock_product_repository.search_product_by = MagicMock(return_value=([sample_product], 1))
        mock_product_repository.update_product = MagicMock()

        with raises(ValueError):
            product_manager.update_or_create(ctx, req, product_id=None)


class TestCreate:
    def test_happy_path(self,
                        ctx, mock_product_repository: ProductRepository, sample_product: Product,
                        product_manager: ProductManager):
        req = FullMutationRequest(
            name='panthere',
            selling_price=999,
            buying_price=99,
        )
        mock_product_repository.create_product = MagicMock()
        mock_product_repository.search_product_by = MagicMock(return_value=([], 0))
        product_manager.update_or_create(ctx, req, product_id=None)

        mock_product_repository.create_product.assert_called_once_with(ctx, name=req.name,
                                                                       selling_price=req.selling_price,
                                                                       buying_price=req.buying_price)


class TestDelete:
    def test_happy_path(self, ctx,
                        mock_product_repository: MagicMock,
                        product_manager: ProductManager):
        # When...
        product_manager.delete(ctx, TEST_PRODUCT_NAME)

        # Expect...
        mock_product_repository.delete_product.assert_called_once_with(ctx, TEST_PRODUCT_NAME)

    def test_not_found(self, ctx,
                       mock_product_repository: MagicMock,
                       product_manager: ProductManager):
        # Given...
        mock_product_repository.delete_product = MagicMock(side_effect=ProductNotFoundError)

        # When...
        with raises(ProductNotFoundError):
            product_manager.delete(ctx, TEST_PRODUCT_NAME)


@fixture
def product_manager(mock_product_repository):
    return ProductManager(
        product_repository=mock_product_repository
    )


@fixture
def mock_product_repository():
    return MagicMock(spec=ProductRepository)


