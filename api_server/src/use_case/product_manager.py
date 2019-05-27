from typing import List, Optional
from dataclasses import dataclass, asdict

from src.entity.product import Product

from src.use_case.interface.product_repository import ProductRepository

from src.exceptions import ProductNotFoundError, IntMustBePositive, StringMustNotBeEmpty, MissingRequiredField

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.util.validator import is_empty

from src.util.context import log_extra
from src.util.log import LOG


# TODO: update_or_create

@dataclass
class PartialMutationRequest:
    """
    Mutation request for a product. This represents the 'diff', that is going to be applied on the product object.

    If a field is set to None, field be left untouched.
    """
    name: str = None
    buying_price: int = None
    selling_price: int = None

    def validate(self):
        # NAME:
        if self.name is not None and not is_empty(self.name):
            raise StringMustNotBeEmpty('name')

        if self.buying_price is not None:
            raise MissingRequiredField('buying_price')

        if self.selling_price is not None:
            raise MissingRequiredField('selling_price')


@dataclass
class FullMutationRequest(PartialMutationRequest):
    """
    Mutation request for a product. This represents the 'diff', that is going to be applied on the product object.

    If a field is set to None, field will be cleared in the database.
    """
    name: str = None
    buying_price: int = None
    selling_price: int = None

    def validate(self):
        # NAME:
        if self.name is None:
            raise MissingRequiredField('name')

        # BUYING_PRICE
        if self.buying_price is None:
            raise MissingRequiredField('buying_price')

        # SELLING_PRICE
        if self.selling_price is None:
            raise MissingRequiredField('selling_price')


class ProductManager:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_by_id(self, ctx, product_id=None) -> Product:
        """
        Search a product in the database.
        """

        result, count = self.product_repository.search_product_by(ctx, product_id=product_id)

        if count == 0:
            raise ProductNotFoundError

        # TODO: LOG.info

        return result[0]

    # TODO: get_by_type and get_by_status (actif or not)

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, product_id=None, terms=None) -> (
            List[Product], int):
        """
        search product in the database.

        user story: as an admin, i want to have a list of products with some filters, so that i can browse and find
        products.

        :raise intmustbepositiveexception
        """
        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.product_repository.search_product_by(ctx,
                                                                  limit=limit,
                                                                  offset=offset,
                                                                  product_id=product_id,
                                                                  terms=terms)

        # Log action.
        LOG.info('product_search', extra=log_extra(
            ctx,
            product_id=product_id,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, req: FullMutationRequest, product_id=None) -> bool:
        req.validate()

        LOG.info('product_update_or_create', extra=log_extra(
            ctx,
            product_id=product_id
        ))

        try:
            result, _ = self.product_repository.search_product_by(ctx, product_id=product_id)
            fields = {k: v for k, v in asdict(req).items()}

        except ProductNotFoundError:
            raise Exception
        if req.name == '':
            raise StringMustNotBeEmpty('name')
        if not req.name:
            raise MissingRequiredField('name')
        if not req.selling_price:
            raise MissingRequiredField('selling_price')
        if not req.buying_price:
            raise MissingRequiredField('buying_price')

        if not result or not product_id:
            LOG.info('product_create', extra=log_extra(
                ctx,
                product_id=product_id
            ))
            # No product with that id/name, creating one...
            self.product_repository.create_product(ctx, **fields)
            return True

        else:
            # A product exists, updating it
            # Warning: ProductNotFound
            LOG.info('product_update', extra=log_extra(
                ctx,
                product_id=product_id,
            ))
            self.product_repository.update_product(ctx, product_id=product_id, **fields)
            return False

    def delete(self, ctx, name) -> None:
        """
        User story: As an admin, I can remove a product, so that their information is not in our system.

        :raise ProductNotFound
        """

        self.product_repository.delete_product(ctx, name)

        # Log action.
        LOG.info('product_delete', extra=log_extra(
            ctx,
            name=name,
        ))