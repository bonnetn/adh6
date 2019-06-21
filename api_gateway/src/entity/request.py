from dataclasses import dataclass


@dataclass
class Request:
    method: str
    args: dict
    headers: dict
    raw_content: bytes
