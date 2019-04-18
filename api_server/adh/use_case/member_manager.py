import logging

from adh.constants import CTX_ADMIN
from adh.exceptions import MustBePositiveException, MemberNotFound
from adh.use_case.interface.member_repository import MemberRepository


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
