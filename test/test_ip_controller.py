from adh.ip_controller import (
    get_available_ip, NoMoreIPAvailable, get_all_used_ip, get_expired_devices
)
from adh.model.database import Database as db
from CONFIGURATION import TEST_DATABASE as db_settings
import pytest


def prep_db(session,
            wired_device):
    session.add_all([
        wired_device,
    ])
    session.commit()


@pytest.fixture
def api_client(wired_device):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                wired_device)
        yield c


@pytest.mark.parametrize('network,taken,expected', [
    ('192.168.102.0/24', [], "192.168.102.1"),
    ('192.168.102.0/24', ["192.168.102.1", "192.168.102.3"], "192.168.102.2"),
    ('192.168.102.0/23', ["192.168.102.1", "192.168.102.3"], "192.168.102.2"),
    (
        '192.168.102.0/23',
        ("192.168.102.{}".format(i) for i in range(256)),
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


def test_get_used_all_ip(api_client):
    s = db.get_db().get_session()
    assert get_all_used_ip(s) == ['157.159.42.42']
