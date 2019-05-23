# coding=utf-8
from dataclasses import dataclass


@dataclass
class PaymentMethod:
    payment_method_id: int
    name: str
