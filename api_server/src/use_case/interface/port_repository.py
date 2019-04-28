# coding=utf-8
"""
Port repository.
"""
import abc
from typing import List

from src.entity.port import Port


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
