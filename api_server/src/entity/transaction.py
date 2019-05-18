# coding=utf-8
from dataclasses import dataclass


@dataclass
class PaymentMethod:
    name: str


@dataclass
class Transaction:
    src: str
    dst: str
    name: str
    value: str
    timestamp: str
    type: PaymentMethod
