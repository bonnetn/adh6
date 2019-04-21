# coding=utf-8
"""
Device repository.
"""
import abc
from typing import List

from src.entity.device import DeviceInfo


class DeviceRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle devices.
    """

    @abc.abstractmethod
    def search_device_by(self, ctx, limit=None, offset=None, username=None, terms=None) -> (List[DeviceInfo], int):
        """
        Search for a device.
        """
        pass  # pragma: no cover
