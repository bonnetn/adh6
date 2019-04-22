from dataclasses import dataclass
from typing import Optional


@dataclass
class Member:
    username: str
    email: str
    first_name: str
    last_name: str
    departure_date: Optional[str]
    comment: Optional[str]
    association_mode: Optional[str]
    room_number: Optional[str]
