from dataclasses import dataclass


class DeviceType:
    Wired = 'wired'
    Wireless = 'wireless'


@dataclass()
class DeviceInfo:
    mac: str
    owner_username: str
    connection_type: str
    ip_address: str
    ipv6_address: str
