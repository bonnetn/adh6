import abc


class IPAllocator(metaclass=abc.ABCMeta):
    """
    Abstract interface to allocate IP addresses.
    """

    @abc.abstractmethod
    def allocate_ip_v4(self, ctx, ip_range: str) -> str:
        """
        Allocates a new unused IP address.

        :raises NoMoreIPAvailable
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def allocate_ip_v6(self, ctx, ip_range: str) -> str:
        """
        Allocates a new unused IP address.

        :raises NoMoreIPAvailable
        """
        pass  # pragma: no cover


class NoMoreIPAvailableException(RuntimeError):
    pass
