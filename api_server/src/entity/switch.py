# coding=utf-8
from dataclasses import dataclass


@dataclass
class Switch:
    id: str
    description: str
    ip_v4: str
    community: str
