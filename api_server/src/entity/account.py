# coding=utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass()
class Account:
    name: str
    type: int
    creation_date: Optional[str]
    actif: Optional[bool]
    account_id: Optional[int]
