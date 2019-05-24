# coding=utf-8
from dataclasses import dataclass


@dataclass()
class AccountType:
    account_type_id: int
    name: str
