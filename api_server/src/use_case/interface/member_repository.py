# coding=utf-8
"""
Member repository interface.
"""
import abc


class NotFoundError(ValueError):
    """
    Object not found in repository.
    """
    pass


class MemberRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to manipulate the members.
    """

    @abc.abstractmethod
    def search_member_by(self, ctx, limit=None, offset=None, room_number=None, terms=None, username=None) -> (
            list, int):
        """
        Search members.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_member(self, ctx, **fields) -> None:
        """
        Create a member.

        :raises NotFoundError
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_member(self, ctx, member_to_update, **fields_to_update) -> None:
        """
        Update a member.

        :raises NotFoundError
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def delete_member(self, ctx, username=None) -> None:
        """
        Delete a member.

        :raises NotFoundError
        """
        pass  # pragma: no cover
