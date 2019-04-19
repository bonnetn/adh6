import abc


class LogFetchError(RuntimeError):
    pass


class LogsRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_logs(self, ctx, username=None, devices=None):
        pass
