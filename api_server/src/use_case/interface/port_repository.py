# coding=utf-8
"""
Port repository.
"""
import abc
from typing import List

from src.entity.port import Port
from src.use_case.interface.member_repository import NotFoundError


class InvalidRoomNumber(NotFoundError):
    pass


class InvalidSwitchID(NotFoundError):
    pass


class PortRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle ports.
    """

    @abc.abstractmethod
    def search_port_by(self, ctx, limit=0, offset=0, port_id: str = None, switch_id: str = None,
                       room_number: str = None, terms: str = None) -> (List[Port], int):
        """
        Search ports.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_port(self, ctx, **fields) -> str:
        """
        Create a port.

        :return the newly created port id
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_port(self, ctx, **fields) -> None:
        """
        Update a port.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def delete_port(self, ctx, port_id: str) -> None:
        """
        Delete a port.
        """
        pass  # pragma: no cover
