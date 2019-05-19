# coding=utf-8
from dataclasses import dataclass


@dataclass()
class Product:
    name: str
    buying_price: float
    selling_price: float

