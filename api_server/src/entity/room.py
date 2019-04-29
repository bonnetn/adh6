# coding=utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class Vlan:
    number: str
    ip_v4_range: str
    ip_v6_range: str


@dataclass
class Room:
    room_number: str
    description: str
    phone_number: Optional[str]  # legacy
    vlan: Vlan
