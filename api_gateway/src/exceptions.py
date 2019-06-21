class AuthException(BaseException):
    pass


class NoStateTokenException(AuthException):
    pass


class NotAuthenticatedException(AuthException):
    pass
