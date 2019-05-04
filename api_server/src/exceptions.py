# coding=utf-8


# INVALID ERRORS.
class InvalidIPv6(ValueError):
    def __init__(self, value):
        super().__init__(f'"{value}" is not a valid IPv6')


class InvalidIPv4(ValueError):
    def __init__(self, value):
        super().__init__(f'"{value}" is not a valid IPv4')


class InvalidMACAddress(ValueError):
    pass  # pragma: no cover


class InvalidAdmin(ValueError):
    pass  # pragma: no cover


class InvalidRoomNumber(ValueError):
    pass


class InvalidSwitchID(ValueError):
    pass


class InvalidEmail(ValueError):
    def __init__(self, mail):
        super().__init__(f'"{mail}" is not a valid email')


class InvalidVLANNumber(ValueError):
    def __init__(self):
        super().__init__('invalid room number')


# NOT FOUND ERROR.

class MemberNotFound(ValueError):
    pass


class DeviceNotFound(Exception):
    pass


class RoomNotFound(ValueError):
    pass  # pragma: no cover


class SwitchNotFound(ValueError):
    pass  # pragma: no cover


class PortNotFound(ValueError):
    pass  # pragma: no cover


class VLANNotFound(ValueError):
    pass  # pragma: no cover


# ALREADY EXIST ERRORS.
class MemberAlreadyExist(ValueError):
    pass


class RoomAlreadyExists(ValueError):
    pass


class DeviceAlreadyExist(Exception):
    pass


# OTHER KIND OF ERRORS.
class UnknownPaymentMethod(ValueError):
    pass  # pragma: no cover


class LogFetchError(RuntimeError):
    """
    Cannot fetch the logs error.
    """
    pass  # pragma: no cover


class ReadOnlyField(ValueError):
    pass


class NoPriceAssignedToThatDurationException(ValueError):
    def __init__(self):
        super().__init__('there is no price assigned to that duration')


class NoMoreIPAvailableException(RuntimeError):
    pass


class UsernameMismatchError(ValueError):
    """
    Thrown when you try to create a member given a username and a mutation request and in the mutation request the
    username does not match the first argument.
    """

    def __init__(self):
        super().__init__('cannot create member with 2 different usernames')


class RoomNumberMismatchError(ValueError):
    """
    Thrown when you try to create a room given a room_number and a mutation request and in the mutation request the
    room_number does not match the first argument.
    """

    def __init__(self):
        super().__init__('cannot create room with 2 different room_numbers')


class MissingRequiredField(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} is missing')


class PasswordTooShortError(ValueError):
    def __init__(self):
        super().__init__('password is too short')


class IntMustBePositiveException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must be positive')


class StringMustNotBeEmptyException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must not be empty')


class InvalidDate(ValueError):
    def __init__(self, value):
        super().__init__(f'"{value}" is not a valid date')


class IPAllocationFailedError(RuntimeError):
    pass
