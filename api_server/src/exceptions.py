# coding=utf-8


class UserInputError(ValueError):
    """
    Type of error thrown when the user input is responsible for the failure of the flow.
    """
    pass


# INVALID ERRORS.
class ValidationError(UserInputError):
    """
    Type of error thrown when we are provided with data that fails the validation.
    """
    pass


class MissingRequiredField(ValidationError):
    def __init__(self, msg):
        super().__init__(f'{msg} is missing')


class InvalidIPv6(ValidationError):
    def __init__(self, v):
        super().__init__(f'"{v}" is not a valid IPv6 address')


class InvalidIPv4(ValidationError):
    def __init__(self, v):
        super().__init__(f'"{v}" is not a valid IPv4 address')


class InvalidMACAddress(ValidationError):
    def __init__(self, v):
        super().__init__(f'"{v}" is not a valid MAC address')


class InvalidEmail(ValidationError):
    def __init__(self, v):
        super().__init__(f'"{v}" is not a valid email')


class InvalidDate(ValidationError):
    def __init__(self, value):
        super().__init__(f'"{value}" is not a valid date')


class InvalidAdmin(ValidationError):
    pass  # pragma: no cover


class PasswordTooShortError(ValidationError):
    def __init__(self):
        super().__init__('password is too short')


class IntMustBePositive(ValidationError):
    def __init__(self, msg):
        super().__init__(f'{msg} must be positive')


class StringMustNotBeEmpty(ValidationError):
    def __init__(self, msg):
        super().__init__(f'{msg} must not be empty')


class NoPriceAssignedToThatDuration(ValidationError):
    def __init__(self, duration):
        super().__init__(f'there is no price assigned to that duration ({duration} days)')


class UsernameMismatchError(ValidationError):
    """
    Thrown when you try to create a member given a username and a mutation request and in the mutation request the
    username does not match the first argument.
    """

    def __init__(self):
        super().__init__('cannot create member with 2 different usernames')


class RoomNumberMismatchError(ValidationError):
    """
    Thrown when you try to create a room given a room_number and a mutation request and in the mutation request the
    room_number does not match the first argument.
    """

    def __init__(self):
        super().__init__('cannot create room with 2 different room_numbers')


# NOT FOUND ERROR.
class NotFoundError(UserInputError):
    """
    Error thrown when something is not found.
    """

    def __init__(self, what, v: str = None):
        err_msg = filter(bool, [what, v, 'is not found'])
        super().__init__(err_msg)


class MemberNotFoundError(NotFoundError):
    def __init__(self, v=None):
        super().__init__('member', v)


class DeviceNotFoundError(NotFoundError):
    def __init__(self, v=None):
        super().__init__('device', v)


class RoomNotFoundError(NotFoundError):
    def __init__(self, v=None):
        super().__init__('room', v)


class SwitchNotFoundError(NotFoundError):
    def __init__(self, v=None):
        v = v or '?'
        super().__init__('switch', f'id={v}')


class PortNotFoundError(NotFoundError):
    def __init__(self, v=None):
        v = v or '?'
        super().__init__('port', f'id={v}')


class VLANNotFoundError(NotFoundError):
    def __init__(self, v=None):
        super().__init__('VLAN', v)


# ALREADY EXIST ERRORS.
class AlreadyExistsError(UserInputError):
    """
    Error thrown when the user tries to create something that already exists.
    """

    def __init__(self, what):
        super().__init__(f'{what} already exists')


class MemberAlreadyExist(AlreadyExistsError):
    def __init__(self, what='member'):
        super().__init__(what)


class RoomAlreadyExists(AlreadyExistsError):
    def __init__(self, what='room'):
        super().__init__(what)


class DeviceAlreadyExist(AlreadyExistsError):
    def __init__(self, what='device'):
        super().__init__(what)

    # OTHER KIND OF ERRORS.


class UnknownPaymentMethod(UserInputError):
    pass  # pragma: no cover


class LogFetchError(RuntimeError):
    """
    Cannot fetch the logs error.
    """
    pass  # pragma: no cover


class NoMoreIPAvailableException(RuntimeError):
    pass  # pragma: no cover
