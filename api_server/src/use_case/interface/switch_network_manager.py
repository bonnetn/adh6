# coding=utf-8
"""
Switch network manager interface.
"""
import abc

from src.entity.port import Port
from src.entity.switch import Switch


class SwitchNetworkManager(metaclass=abc.ABCMeta):
    """
    Abstract interface to manipulate the members.
    """

    @abc.abstractmethod
    def get_port_status(self, ctx, switch: Switch = None, port: Port = None) -> bool:
        """
        Retrieve the status of a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_port_status(self, ctx, switch: Switch = None, port: Port = None, status=None) -> None:
        """
        Update the status of a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_port_vlan(self, ctx, switch: Switch = None, port: Port = None) -> int:
        """
        Get the VLAN assigned to a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_port_vlan(self, ctx, switch: Switch = None, port: Port = None, vlan=None) -> None:
        """
        Update the VLAN assigned to a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_port_mab(self, ctx, switch: Switch = None, port: Port = None) -> bool:
        """
        Retrieve whether MAB is active on a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def update_port_mab(self, ctx, switch: Switch = None, port: Port = None, mab=None) -> None:
        """
        Update whether MAB should be active on a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover
