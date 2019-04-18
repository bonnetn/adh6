import json
import logging

from attr import dataclass, asdict

from adh.constants import CTX_ADMIN, CTX_SQL_SESSION
from adh.exceptions import MustBePositiveException, MemberNotFound
from adh.use_case.interface.member_repository import MemberRepository
from adh.util.checks import is_email


@dataclass
class MutationRequest:
    email: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    departure_date: str = None
    comment: str = None
    association_mode: str = None
    room_number: int = None


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

        logging.info("%s fetched the member %s", ctx.get(CTX_ADMIN), username)
        return result[0]

    def search(self, ctx, limit, offset=0, room_number=None, terms=None):
        if limit < 0:
            raise MustBePositiveException('limit')

        if offset < 0:
            raise MustBePositiveException('offset')

        result, count = self.member_storage.search_member_by(ctx,
                                                             limit=limit,
                                                             offset=offset,
                                                             room_number=room_number,
                                                             terms=terms)

        logging.info("%s fetched the member list", ctx.get(CTX_ADMIN))
        return result, count

    def delete(self, ctx, username):
        if not username:
            raise ValueError('username not provided')

        try:
            self.member_storage.delete_member(ctx, username)
            logging.info("%s deleted the member %s", ctx.get(CTX_ADMIN), username)
        except ValueError:
            raise MemberNotFound()

    def update_partially(self, ctx, username, mutation_request: MutationRequest):
        admin = ctx.get(CTX_ADMIN)

        if mutation_request.email is not None and not is_email(mutation_request.email):
            raise ValueError('invalid email')

        if mutation_request.first_name == '':
            raise ValueError('first name must not be empty')

        if mutation_request.last_name == '':
            raise ValueError('last name must not be empty')

        if mutation_request.username == '':
            raise ValueError('username must not be empty')

        if mutation_request.comment == '':
            raise ValueError('comment must not be empty')

        if mutation_request.room_number is not None and mutation_request.room_number < 0:
            raise ValueError('room number must not be negative')

        self.member_storage.update_partially_member(ctx, username, **asdict(mutation_request))

        logging.info("%s updated the member %s\n%s",
                     admin.login, username, json.dumps(asdict(mutation_request), sort_keys=True))
