# coding=utf-8
"""
Logs repository interface.
"""
import abc


class LogFetchError(RuntimeError):
    """
    Cannot fetch the logs error.
    """
    pass


class LogsRepository(metaclass=abc.ABCMeta):
    """
    Abstract interface to access the logs.
    """
    @abc.abstractmethod
    def get_logs(self, ctx, username=None, devices=None):
        """
        Get all the logs concerning the provided username and MAC addresses.
        """
        pass
