from adh.ip_controller import get_available_ip, NoMoreIPAvailable
import pytest


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
