import datetime

import pytest

from adh.model.models import (
    Adherent, Chambre, Vlan, Ordinateur, Portable, Switch, Port
)


@pytest.fixture
def wired_device(sample_member1):
    yield Ordinateur(
        mac='96-24-F6-D0-48-A7',
        ip='157.159.42.42',
        dns='bonnet_n4651',
        adherent=sample_member1,
        ipv6='e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4'
    )


@pytest.fixture
def wired_device2(sample_member3):
    yield Ordinateur(
        mac='96-24-F6-D0-48-A8',
        ip='157.159.43.43',
        dns='test',
        adherent=sample_member3,
        ipv6='f91f:bd71:56d9:13f3:5499:25b:cc84:f7e4'
    )


@pytest.fixture
def wireless_device(sample_member2):
    yield Portable(
        mac='80-65-F3-FC-44-A9',
        adherent=sample_member2,
    )


@pytest.fixture
def wireless_device_dict():
    '''
    Device that will be inserted/updated when tests are run.
    It is not present in the api_client by default
    '''
    yield {
        'mac': '01-23-45-67-89-AC',
        'connectionType': 'wireless',
        'username': 'dubois_j'
    }


@pytest.fixture
def wired_device_dict():
    yield {
        'mac': '01-23-45-67-89-AD',
        'ipAddress': '127.0.0.1',
        'ipv6Address': 'dbb1:39b7:1e8f:1a2a:3737:9721:5d16:166',
        'connectionType': 'wired',
        'username': 'dupontje'
    }


@pytest.fixture
def sample_vlan():
    yield Vlan(
        numero=42,
        adresses="192.168.42.0/24",
        adressesv6="fe80::0/64",
    )


@pytest.fixture
def sample_room1(sample_vlan):
    yield Chambre(
        numero=5110,
        description="Chambre de l'ambiance",
        telephone=1234,
        vlan=sample_vlan,
    )


@pytest.fixture
def sample_room2(sample_vlan):
    yield Chambre(
        numero=4592,
        description="Chambre voisine du swag",
        telephone="5678",
        vlan=sample_vlan,
    )


@pytest.fixture
def sample_member1(sample_room1):
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='a',
        chambre=sample_room1,
        date_de_depart=datetime.datetime(2005, 7, 14, 12, 30),
    )


@pytest.fixture
def sample_member2(sample_room1):
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        commentaires='Desauthent pour routeur',
        password='a',
        chambre=sample_room1,
    )


@pytest.fixture
def sample_member3(sample_room1):
    yield Adherent(
        nom='Dupont',
        prenom='Jean',
        mail='test@oyopmail.fr',
        login='dupontje',
        commentaires='abcdef',
        password='b',
        chambre=sample_room1,
        date_de_depart=datetime.datetime(2105, 7, 14, 12, 30),
    )


@pytest.fixture
def sample_switch1():
    yield Switch(
        description="Switch sample 1",
        ip="192.168.102.51",
        communaute="GrosMotDePasse",
    )


@pytest.fixture
def sample_switch2():
    yield Switch(
        description="Switch sample 2",
        ip="192.168.102.52",
        communaute="GrosMotDePasse",
    )


@pytest.fixture
def sample_port1(sample_switch1):
    yield Port(
        rcom=1,
        numero="0/0/1",
        oid="1.1.1",
        switch=sample_switch1,
        chambre_id=0,

    )


@pytest.fixture
def sample_port2(sample_switch2):
    yield Port(
        rcom=2,
        numero="0/0/2",
        oid="1.1.2",
        switch=sample_switch2,
        chambre_id=0,

    )
