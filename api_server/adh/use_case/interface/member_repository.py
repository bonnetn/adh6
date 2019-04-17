import abc


class MemberRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search_member_by(self, ctx, limit=None, offset=None, room_number=None, terms=None) -> (list, int):
        pass
