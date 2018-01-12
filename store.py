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
        'username': 'coroller'
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

for k, v in PORTS.items():
    v["_id"] = k

port_id = 42

ROOMS = {
    1111: {
        'description': "Chambre 1111",
        'roomNumber': 1111,
        'phone': 0,
        'vlan': 41
    },
    1234: {
        'description': "Chambre 1234",
        'roomNumber': 1234,
        'phone': 0,
        'vlan': 41
    }
}

SWITCHES = {
    1: {
        'description': "Switch U1",
        'ip': "192.168.102.11",
        'community': "tototo"
    },
    2: {
        'description': "Switch U2",
        'ip': "192.168.102.12",
        'community': "tututu"
    },
    3: {
        'description': "Switch-local",
        'ip': "192.168.102.12",
        'community': "tirelinpimpon"
    },
}

for k, v in SWITCHES.items():
    v["_id"] = k

switch_id = 42

USERS = {
    "coroller": {
        "email": "stevan.coroller@telecom-em.eu",
        "firstName": "Stevan",
        "lastName": "Coroller",
        "username": "coroller",
        "comment": "Desauthent pour routeur",
        "roomNumber": 1111,
        "departureDate": "2017-12-13 00:00:00",
        "associationMode": "2017-01-01 00:00:00"
    },
    "cherre_r": {
        "email": "romain.cherre@telecom-em.eu",
        "firstName": "Romain",
        "lastName": "Cherré",
        "username": "cherre_r",
        "comment": "Mdr",
        "roomNumber": 1111,
        "departureDate": "2017-12-13 00:00:00",
        "associationMode": "2017-01-01 00:00:00"
    },
    "coutelou": {
        "email": "thomas.coutelou@telecom-sudparis.eu",
        "firstName": "Thomas",
        "lastName": "Coutelou",
        "username": "coutelou",
        "comment": "Desauthent pour PS4",
        "roomNumber": 1234,
        "departureDate": "2017-12-13 00:00:00",
        "associationMode": "2017-01-01 00:00:00"
    }

}


def get_db():
    if not hasattr(g, "db_session"):
        g.db_session = {
            "DEVICES": DEVICES,
            "PORTS": PORTS,
            "port_id": port_id,
            "ROOMS": ROOMS,
            "SWITCHES": SWITCHES,
            "switch_id": switch_id,
            "USERS": USERS,
        }
    return g.db_session


def disconnect_db():
    pass
