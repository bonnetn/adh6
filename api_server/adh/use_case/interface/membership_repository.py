import abc


class MembershipRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_membership(self, ctx, username, start, end):
        pass
