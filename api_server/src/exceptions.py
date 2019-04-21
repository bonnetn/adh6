class InvalidEmail(ValueError):
    pass


class InvalidIPv6(ValueError):
    pass


class InvalidIPv4(ValueError):
    pass


class InvalidMac(ValueError):
    pass


class MemberNotFound(ValueError):
    pass


class SwitchNotFound(ValueError):
    pass


class PortNotFound(ValueError):
    pass


class VlanNotFound(ValueError):
    pass


class RoomNotFound(ValueError):
    pass


class IntMustBePositiveException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must be positive')


class StringMustNotBeEmptyException(ValueError):
    def __init__(self, msg):
        super().__init__(f'{msg} must not be empty')
