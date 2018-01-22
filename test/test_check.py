import pytest

from controller import checks
from test import resource


@pytest.mark.parametrize('mac', [
    "12:34:56:78:9A:BC",   # OK
    "DE:F0:00:00:00:00",
    "12:34:56:78:9a:bc",   # lowercased, OK
])
def test_check_valid_mac(mac):
    assert checks.isMac(mac) is True


@pytest.mark.parametrize('mac', resource.INVALID_MAC)
def test_check_invalid_mac(mac):
    assert checks.isMac(mac) is False
