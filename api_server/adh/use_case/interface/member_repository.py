import abc


class MemberRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search_member_by(self, ctx, limit=None, offset=None, room_number=None, terms=None, username=None) -> (list, int):
        pass

    @abc.abstractmethod
    def update_partially_member(self, ctx, member_to_update, **fields_to_update) -> None:
        pass

    @abc.abstractmethod
    def delete_member(self, ctx, username=None) -> None:
        pass
