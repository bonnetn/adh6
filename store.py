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

PORTS = {
    0: {
        'portNumber': '1/0/4',
        'roomNumber': 1234,
        'switchID': 1,
    },
    1: {
        'portNumber': '1/0/3',
        'roomNumber': 1111,
        'switchID': 2,
    },
    2: {
        'portNumber': '1/0/7',
        'roomNumber': 1111,
        'switchID': 3,
    },
    3: {
        'portNumber': '1/0/8',
        'roomNumber': 1234,
        'switchID': 1,
    }
}

for k,v in PORTS.items():
    v["_id"] = k

port_id = 42


def get_db():
    if not hasattr(g, "db_session"):
        g.db_session = {
            "DEVICES": DEVICES,
            "PORTS": PORTS,
            "port_id": port_id
        }
    return g.db_session


def disconnect_db():
    pass
