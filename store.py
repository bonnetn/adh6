from flask import g

DEVICES = {
    "6C:C2:17:67:89:AB": {
        'mac': '6C:C2:17:67:89:AB',
        'ipAddress': '157.159.42.1',
        'ipv6Address': 'ff02::1',
        'connectionType': 'wired',
        'username': 'coroller'
    },
    "14:2D:27:FA:73:FF": {
        'mac': '14:2D:27:FA:73:FF',
        'ipAddress': '157.159.42.2',
        'ipv6Address': 'ff02::2',
        'connectionType': 'wireless',
        'username'	: 'coroller'
    }
}


def get_db():
    if not hasattr(g, "db_session"):
        g.db_session = {
            "DEVICES": DEVICES,
        }
    return g.db_session


def disconnect_db():
    pass
