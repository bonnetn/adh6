# coding=utf-8
"""
Switch repository.
"""
import abc
from typing import List

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.switch import Switch


class SwitchRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle switches.
    """

    @abc.abstractmethod
    def search_switches_by(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, switch_id: str = None,
                           terms: str = None) -> (
            List[Switch], int):
        """
        Search switches.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_switch(self, ctx, **fields) -> str:
        """
        Create a switch.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_switch(self, ctx, switch_id, **fields) -> None:
        """
        Update a switch.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def delete_switch(self, ctx, switch_id: str) -> None:
        """
        Delete a switch.
        """
        pass  # pragma: no cover
