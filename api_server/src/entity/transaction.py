# coding=utf-8
from dataclasses import dataclass

from src.entity.payment_method import PaymentMethod


@dataclass
class Transaction:
    src: str
    dst: str
    name: str
    value: str
    timestamp: str
    attachments: str
    payment_method: PaymentMethod
