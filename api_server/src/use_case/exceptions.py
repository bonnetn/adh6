class MemberAlreadyExist(ValueError):
    pass


class MemberNotFound(ValueError):
    pass


class UsernameMismatchError(ValueError):
    """
    Thrown when you try to create a member given a username and a mutation request and in the mutation request the
    username does not match the first argument.
    """

    def __init__(self):
        super().__init__('cannot create member with 2 different usernames')


class MissingRequiredFieldError(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} is missing')


class PasswordTooShortError(ValueError):
    def __init__(self):
        super().__init__('password is too short')


class InvalidEmailError(ValueError):
    def __init__(self):
        super().__init__('email is invalid')


class InvalidRoomNumberError(ValueError):
    def __init__(self):
        super().__init__('invalid room number')


class IntMustBePositiveException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must be positive')


class StringMustNotBeEmptyException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must not be empty')


class DeviceAlreadyExist(Exception):
    pass


class DeviceNotFound(Exception):
    pass


class IPAllocationFailedError(RuntimeError):
    pass
