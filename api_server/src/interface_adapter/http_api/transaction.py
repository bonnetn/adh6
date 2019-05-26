# coding=utf-8
from dataclasses import asdict

from connexion import NoContent

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.transaction import Transaction
from src.exceptions import UserInputError, TransactionNotFoundError
from src.interface_adapter.http_api.account import _map_account_to_http_response
from src.interface_adapter.http_api.decorator.with_context import with_context
from src.interface_adapter.http_api.payment_method import _map_payment_method_to_http_response
from src.interface_adapter.http_api.util.error import bad_request
from src.interface_adapter.sql.decorator.auth import auth_regular_admin
from src.interface_adapter.sql.decorator.sql_session import require_sql
from src.use_case.transaction_manager import TransactionManager, PartialMutationRequest, FullMutationRequest
from src.util.context import log_extra
from src.util.log import LOG


class TransactionHandler:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager

    @with_context
    @require_sql
    @auth_regular_admin
    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, account_id=None, terms=None):
        """ Search all the member. """
        LOG.debug("http_transaction_search_called", extra=log_extra(ctx,
                                                                    limit=limit,
                                                                    offset=offset,
                                                                    account_id=account_id,
                                                                    terms=terms))
        try:
            result, total_count = self.transaction_manager.search(ctx, limit, offset, account_id, terms)
            headers = {
                "X-Total-Count": str(total_count),
                'access-control-expose-headers': 'X-Total-Count'
            }
            result = list(map(_map_transaction_to_http_response, result))
            return result, 200, headers  # 200 OK

        except UserInputError as e:
            return bad_request(e), 400  # 400 Bad Request

    @with_context
    @require_sql
    @auth_regular_admin
    def get(self, ctx, transaction_id):
        """ Get a specific transaction. """
        LOG.debug("http_transaction_get_called", extra=log_extra(ctx, transaction_id=transaction_id))
        try:
            return _map_transaction_to_http_response(
                self.transaction_manager.get_by_id(ctx, transaction_id)), 200  # 200 OK

        except TransactionNotFoundError:
            return NoContent, 404  # 404 Not Found

    @with_context
    @require_sql
    @auth_regular_admin
    def post(self, ctx, body):
        """ Add a transaction record in the database """
        LOG.debug("http_transaction_post_called", extra=log_extra(ctx, request=body))

        mutation_request = _map_http_request_to_full_mutation_request(body)
        try:
            created = self.transaction_manager.update_or_create(ctx, mutation_request)
            if created:
                return NoContent, 201  # 201 Created
            else:
                return NoContent, 204  # 204 No Content

        except UserInputError as e:
            return bad_request(e), 400  # 400 Bad Request

    @with_context
    @require_sql
    @auth_regular_admin
    def put(self, ctx, transaction_id, body):
        pass


def _map_transaction_to_http_response(transaction: Transaction) -> dict:
    fields = {
        "src": _map_account_to_http_response(transaction.src),
        "dst": _map_account_to_http_response(transaction.dst),
        "timestamp": transaction.timestamp,
        "name": transaction.name,
        "paymentMethod": _map_payment_method_to_http_response(transaction.paymentMethod),
        "value": transaction.value,
        "attachments": transaction.attachments
    }

    return {k: v for k, v in fields.items() if v is not None}


def _map_http_request_to_partial_mutation_request(body) -> PartialMutationRequest:
    return PartialMutationRequest(
        src=body.get('src_id'),
        dst=body.get('dst_id'),
        name=body.get('name'),
        paymentMethod=body.get('payment_method_id'),
        value=body.get('value')
    )


def _map_http_request_to_full_mutation_request(body) -> FullMutationRequest:
    partial = _map_http_request_to_partial_mutation_request(body)
    return FullMutationRequest(**asdict(partial))
