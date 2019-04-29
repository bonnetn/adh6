# coding=utf-8
from dateutil import parser
from typing import Optional


def string_to_date(s):
    """ Converts a ISO 8601 date formatted string to a python datetime """
    if not s:
        return None

    return parser.parse(s)


def date_to_string(d) -> Optional[str]:
    if d is None:
        return d

    return d.isoformat()
