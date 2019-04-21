from dataclasses import dataclass


@dataclass
class Member:
    username: str
    email: str
    first_name: str
    last_name: str
    departure_date: str
    comment: str
    association_mode: str
    room_number: str


@dataclass
class Admin:
    login: str
