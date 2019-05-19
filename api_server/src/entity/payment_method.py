# coding=utf-8
from dataclasses import dataclass


@dataclass
class PaymentMethod:
    id: int
    name: str
