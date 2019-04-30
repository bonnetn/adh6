import abc

from src.entity.vlan import Vlan


class VLANRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to handle VLANs.
    """

    @abc.abstractmethod
    def get_vlan(self, ctx, vlan_number) -> Vlan:
        """
        Get a VLAN.

        :raises NotFoundError
        """
        pass  # pragma: no cover
