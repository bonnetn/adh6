import pytest
from adh.model.models import Ordinateur, Portable, Adherent

@pytest.fixture
def member1():
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='a',
    )


@pytest.fixture
def member2():
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        password='b',
    )


@pytest.fixture
def wired_device(member1):
    yield Ordinateur(
        mac='96:24:F6:D0:48:A7',
        ip='157.159.42.42',
        dns='bonnet_n4651',
        adherent=member1,
        ipv6='e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4'
    )


@pytest.fixture
def wireless_device(member2):
    yield Portable(
        mac='80:65:F3:FC:44:A9',
        adherent=member2,
    )


@pytest.fixture
def wireless_device_dict():
    '''
    Device that will be inserted/updated when tests are run.
    It is not present in the api_client by default
    '''
    yield {
      'mac': '01:23:45:67:89:AC',
      'ipAddress': '127.0.0.1',
      'ipv6Address': 'c69f:6c5:754c:d301:df05:ba81:76a8:ddc4',
      'connectionType': 'wireless',
      'username': 'dubois_j'
    }


@pytest.fixture
def wired_device_dict():
    yield {
      'mac': '01:23:45:67:89:AD',
      'ipAddress': '127.0.0.1',
      'ipv6Address': 'dbb1:39b7:1e8f:1a2a:3737:9721:5d16:166',
      'connectionType': 'wired',
      'username': 'dubois_j'
    }



