import json
import logging
from enum import Enum

from attr import dataclass, asdict

from adh.constants import CTX_ADMIN
from adh.exceptions import IntMustBePositiveException, MemberNotFound, StringMustNotBeEmptyException
from adh.use_case.interface.member_repository import MemberRepository
from adh.util.checks import is_email


class Mutation(Enum):
    NOT_SET = 1


@dataclass
class MutationRequest:
    email: str = Mutation.NOT_SET
    first_name: str = Mutation.NOT_SET
    last_name: str = Mutation.NOT_SET
    username: str = Mutation.NOT_SET
    departure_date: str = Mutation.NOT_SET
    comment: str = Mutation.NOT_SET
    association_mode: str = Mutation.NOT_SET
    room_number: int = Mutation.NOT_SET


class MemberManager:
    def __init__(self,
                 member_storage: MemberRepository):
        self.member_storage = member_storage

    def get_by_username(self, ctx, username):
        if not username:
            raise ValueError('username not provided')

        result, _ = self.member_storage.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFound()

        # Log action.
        logging.info("%s fetched the member %s", ctx.get(CTX_ADMIN), username)
        return result[0]

    def search(self, ctx, limit, offset=0, room_number=None, terms=None):
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.member_storage.search_member_by(ctx,
                                                             limit=limit,
                                                             offset=offset,
                                                             room_number=room_number,
                                                             terms=terms)

        # Log action.
        logging.info("%s fetched the member list", ctx.get(CTX_ADMIN))
        return result, count

    def delete(self, ctx, username):
        if not username:
            raise ValueError('username not provided')

        try:
            self.member_storage.delete_member(ctx, username)

            # Log action.
            logging.info("%s deleted the member %s", ctx.get(CTX_ADMIN), username)
        except ValueError:
            raise MemberNotFound()

    def update_partially(self, ctx, username, mutation_request: MutationRequest):
        # Perform all the checks on the validity of the data in the mutation request.
        _validate_mutation_request(mutation_request)

        # Create a dict with all the changed field. If a field in 'NOT_SET' it will not be put in the dict, and the
        # field will not be updated.
        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if _is_set(v)}

        self.member_storage.update_member(ctx, username, **fields_to_update)

        # Log action.
        admin = ctx.get(CTX_ADMIN)
        logging.info("%s updated the member %s\n%s",
                     admin.login, username, json.dumps(fields_to_update, sort_keys=True))

    def create_or_update(self, ctx, username, mutation_request: MutationRequest) -> bool:
        """
        Create/Update member from the database.
        :return: True if the member was created, false otherwise.
        """
        admin = ctx.get(CTX_ADMIN)

        # Make sure all the fields set are valid.
        _validate_mutation_request(mutation_request)

        member, _ = self.member_storage.search_member_by(ctx, username=username)
        if member:
            # [UPDATE] Member already exists, perform a whole update.

            # Make sure all the necessary fields are set.
            if not _is_set(mutation_request.username):
                raise ValueError('username is a required field')


            # Create a dict with fields to update. If field is not provided in the mutation request, consider that it
            # should be None as it is a full update of the member.
            fields_to_update = asdict(mutation_request)
            fields_to_update = {k: v if _is_set(v) else None for k, v in fields_to_update.items()}

            self.member_storage.update_member(ctx, username, **fields_to_update)

            # Log action.
            logging.info("%s updated the member %s\n%s",
                         admin.login, username, json.dumps(fields_to_update, sort_keys=True))

            return False
        else:
            # [CREATE] Member does not exist, create it.

            # Build a dict that will be transformed into a member. If a field is not set, consider that it should be
            # None.
            if _is_set(mutation_request.username) and username != mutation_request.username:
                raise ValueError('cannot create member with 2 different usernames')

            mutation_request.username = username  # Just in case it has not been specified in the body.
            fields = asdict(mutation_request)
            fields = {k: v if _is_set(v) else None for k, v in fields.items()}

            self.member_storage.create_member(ctx, **fields)

            # Log action
            logging.info("%s created the member %s\n%s",
                         admin.login, username, json.dumps(fields, sort_keys=True))

            return True


def _is_set(v):
    """
    Check if a field in a MutationRequest is set.
    """
    return v != Mutation.NOT_SET


def _validate_mutation_request(req: MutationRequest):
    """
    Validate the fields that are set in a MutationRequest.
    """
    if _is_set(req.email) and not is_email(req.email):
        raise ValueError('invalid email')

    if req.first_name == '':
        raise StringMustNotBeEmptyException('first_name')

    if req.last_name == '':
        raise StringMustNotBeEmptyException('last_name')

    if req.username == '':
        raise StringMustNotBeEmptyException('username')

    if req.comment == '':
        raise StringMustNotBeEmptyException('comment')

    if _is_set(req.room_number) and req.room_number < 0:
        raise StringMustNotBeEmptyException('room number')
