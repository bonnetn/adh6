from dateutil import parser


def string_to_date(s):
    """ Converts a ISO 8601 date formatted string to a python datetime """
    if not s:
        return None
    return parser.parse(s)
