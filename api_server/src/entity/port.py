# coding=utf-8
from dataclasses import dataclass


@dataclass
class SwitchInfo:
    switch_id: str
    rcom: int
    oid: str


@dataclass
class Port:
    id: str
    port_number: str
    room_number: str
    switch_info: SwitchInfo
