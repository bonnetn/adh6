from adh.model.models import Ordinateur
from adh.ip_controller import (
    get_available_ip, NoMoreIPAvailable, get_all_used_ipv4, get_all_used_ipv6,
    get_expired_devices, free_expired_devices
)
from adh.model.database import Database as db
from CONFIGURATION import TEST_DATABASE as db_settings
import pytest


def prep_db(session,
            wired_device,
            wired_device2):
    session.add_all([
        wired_device,
        wired_device2,
    ])
    session.commit()


@pytest.fixture
def api_client(wired_device, wired_device2):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                wired_device, wired_device2)
        yield c


@pytest.mark.parametrize('network,taken,expected', [
    ('192.168.102.0/24', [], "192.168.102.2"),
    ('192.168.102.0/24', ["192.168.102.2", "192.168.102.4"], "192.168.102.3"),
    ('192.168.102.0/23', ["192.168.102.2", "192.168.102.4"], "192.168.102.3"),
    (
        '192.168.102.0/23',
        ("192.168.102.{}".format(i) for i in range(2, 256)),
        "192.168.103.0"
    ),
])
def test_assigment_ip(network, taken, expected):
    assert get_available_ip(network, taken) == expected


@pytest.mark.parametrize('network,taken', [
    ('192.168.102.0/24', ["192.168.102.{}".format(i) for i in range(256)]),
    ('192.168.102.0/25', ["192.168.102.{}".format(i) for i in range(128)]),
    ('192.168.102.0/32', []),
])
def test_assigment_ip_no_more_left(network, taken):
    with pytest.raises(NoMoreIPAvailable):
        print(get_available_ip(network, taken))


def test_get_expired_devices(api_client):
    s = db.get_db().get_session()
    expired = get_expired_devices(s)
    expired = list(map(lambda x: x.mac, expired))
    assert expired == ['96:24:F6:D0:48:A7']


def test_free_expired_devices(api_client):
    s = db.get_db().get_session()
    free_expired_devices(s)
    q = s.query(Ordinateur)
    q = q.filter(Ordinateur.mac == '96:24:F6:D0:48:A7')
    assert q.one().ip == "En Attente"


def test_get_used_all_ipv4(api_client):
    s = db.get_db().get_session()
    assert sorted(get_all_used_ipv4(s)) == ['157.159.42.42', '157.159.43.43']


def test_get_used_all_ipv6(api_client):
    s = db.get_db().get_session()
    assert sorted(get_all_used_ipv6(s)) == [
        'e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4',
        'f91f:bd71:56d9:13f3:5499:25b:cc84:f7e4'
    ]