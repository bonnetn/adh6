# coding=utf-8
"""
Device repository.
"""
import abc
from typing import List

from src.entity.device import Device


class DeviceRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle devices.
    """

    @abc.abstractmethod
    def search_device_by(self, ctx, limit=None, offset=None, mac_address=None, username=None, terms=None) -> \
            (List[Device], int):
        """
        Search for a device.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_device(self, ctx, mac_address=None, owner_username=None, connection_type=None, ip_v4_address=None,
                      ip_v6_address=None):
        """
        Create a device.
        """
        pass  # pragma: no cover

    def update_device(self, ctx, mac_address, owner_username=None, connection_type=None, ip_v4_address=None,
                      ip_v6_address=None):
        """
        Update a device.
        """
        pass  # pragma: no cover
