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


def MustBePositiveException(name):
    return ValueError(f'{name} must be positive')
