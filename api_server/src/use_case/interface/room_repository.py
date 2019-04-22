# coding=utf-8
"""
Room repository.
"""
import abc
from typing import List

from src.entity.room import Room


class RoomRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle rooms.
    """

    @abc.abstractmethod
    def search_room_by(self, ctx, owner_username=None) -> (List[Room], int):
        """
        Search rooms.
        """
        pass  # pragma: no cover
