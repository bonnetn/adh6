# coding=utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass()
class Product:
    name: str
    buying_price: int
    selling_price: int
    product_id: Optional[int]
