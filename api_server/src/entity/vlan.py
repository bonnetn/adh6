# coding=utf-8
from dataclasses import dataclass


@dataclass
class Vlan:
    number: str
    ip_v4_range: str
    ip_v6_range: str
