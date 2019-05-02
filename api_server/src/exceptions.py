# coding=utf-8
class InvalidEmail(ValueError):
    pass


class InvalidIPv6(ValueError):
    pass


class InvalidIPv4(ValueError):
    pass


class InvalidMac(ValueError):
    pass


class SwitchNotFound(ValueError):
    pass


class PortNotFound(ValueError):
    pass


class VlanNotFound(ValueError):
    pass


class RoomNotFound(ValueError):
    pass


class InvalidAdmin(ValueError):
    pass


class UnknownPaymentMethod(ValueError):
    pass
