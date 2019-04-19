# coding=utf-8
"""
Membership repository.
"""
import abc


class MembershipRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle memberships.
    """
    @abc.abstractmethod
    def add_membership(self, ctx, username, start, end):
        """
        Add a membership.
        """
        pass
