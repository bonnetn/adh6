import json
import pytest
from model.database import Database as db
from model.models import Chambre, Vlan
from unit_test_settings import DATABASE as db_settings
from .resource import base_url


@pytest.fixture
def sample_vlan():
    yield Vlan(
        numero=42,
        adresses="192.168.1.0/24",
        adressesv6="fe80::0",
    )


@pytest.fixture
def sample_room1(sample_vlan):
    yield Chambre(
        numero=4591,
        description="Chambre du swag",
        telephone="1234",
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


def prep_db(session,
            sample_room1,
            sample_room2,
            sample_vlan):
    session.add_all([
        sample_vlan,
        sample_room1,
        sample_room2,
    ])
    session.commit()


@pytest.fixture
def api_client(sample_room1, sample_room2, sample_vlan):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_room1, sample_room2, sample_vlan)
        yield c


def test_room_filter_all_rooms(api_client):
    r = api_client.get("{}/room/".format(base_url))
    assert r.status_code == 200

    response = json.loads(r.data.decode())
    assert len(response) == 2


def test_room_filter_all_rooms_limit(api_client):
    r = api_client.get("{}/room/?limit={}".format(base_url, 1))
    assert r.status_code == 200

    response = json.loads(r.data.decode())
    assert len(response) == 1
