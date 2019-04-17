from attr import dataclass


@dataclass
class Member:
    first_name: str
    last_name: str
    email: str
