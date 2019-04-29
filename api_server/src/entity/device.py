# coding=utf-8
from dataclasses import dataclass
from typing import Optional


class DeviceType:
    Wired = 'wired'
    Wireless = 'wireless'


@dataclass()
class Device:
    mac_address: str
    owner_username: str
    connection_type: str
    ip_v4_address: Optional[str]
    ip_v6_address: Optional[str]
