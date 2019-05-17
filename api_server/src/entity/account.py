# coding=utf-8
from dataclasses import dataclass
from typing import Optional
from src.entity.account_type import AccountType


@dataclass()
class Account:
    name: str
    type: AccountType
    creation_date: Optional[str]
    actif: Optional[bool]
