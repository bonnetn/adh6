import json
import pytest
from model.database import Database as db
from adh.settings.unit_test_settings import DATABASE as db_settings
from model.models import Port, Switch

from .resource import base_url


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


def prep_db(session,
            sample_switch1,
            sample_switch2,
            sample_port1,
            sample_port2):
    session.add_all([
        sample_switch1,
        sample_switch2,
        sample_port1,
        sample_port2
    ])
    session.commit()


@pytest.fixture
def api_client(sample_port1, sample_port2, sample_switch1, sample_switch2):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_switch1,
                sample_switch2,
                sample_port1,
                sample_port2)
        yield c


def test_port_to_dict(sample_port1):
    dict(sample_port1)


def test_port_get_filter_all(api_client):
    r = api_client.get("{}/ports/".format(base_url))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 2


def test_port_get_filter_all_with_limit(api_client):
    r = api_client.get("{}/ports/?limit=1".format(base_url))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 1


def test_port_get_filter_by_switchid(api_client, sample_switch2):
    r = api_client.get(
        "{}/ports/?switchID={}".format(base_url, sample_switch2.id))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 1


def test_port_get_filter_by_roomnumber_with_results(api_client):
    r = api_client.get(
        "{}/ports/?roomNumber={}".format(base_url, 0))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 2


def test_port_get_filter_by_roomnumber_without_result(api_client):
    r = api_client.get(
        "{}/ports/?roomNumber={}".format(base_url, 42))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert not switches
    assert len(switches) == 0


def test_port_get_filter_by_term_oid(api_client):
    r = api_client.get(
        "{}/ports/?terms={}".format(base_url, "1.2"))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 1


def test_port_get_filter_by_term_numero(api_client):
    r = api_client.get(
        "{}/ports/?terms={}".format(base_url, "0/0/1"))
    assert r.status_code == 200
    switches = json.loads(r.data.decode())
    assert switches
    assert len(switches) == 1


def test_port_post_create_port(api_client, sample_switch1):
    body = {
      "roomNumber": 5110,
      "switchID": sample_switch1.id,
      "portNumber": "1/0/4"
    }

    r = api_client.post(
        "{}/switch/{}/port/".format(base_url, sample_switch1.id),
        data=json.dumps(body),
        content_type='application/json')
    assert r.status_code == 200
    assert 'Location' in r.headers


def test_port_get_existant_port(api_client, sample_switch1, sample_port1):
    r = api_client.get(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      sample_port1.id))
    assert r.status_code == 200
    switch = json.loads(r.data.decode())
    assert switch


def test_port_get_non_existant_port(api_client, sample_switch1, sample_port1):
    r = api_client.get(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      4242))
    assert r.status_code == 404


def test_port_put_update_port(api_client, sample_switch1, sample_port1):

    portNumber = "1/2/3"
    body = {
      "roomNumber": 5110,
      "switchID": sample_switch1.id,
      "portNumber": portNumber
    }

    assert sample_port1.numero != portNumber
    r = api_client.put(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      sample_port1.id),
        data=json.dumps(body),
        content_type='application/json')
    assert r.status_code == 204
    assert sample_port1.numero == portNumber


def test_port_put_update_non_existant_port(api_client,
                                           sample_switch1):

    portNumber = "1/2/3"
    body = {
      "roomNumber": 5110,
      "switchID": sample_switch1.id,
      "portNumber": portNumber
    }

    r = api_client.put(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      4242),
        data=json.dumps(body),
        content_type='application/json')
    assert r.status_code == 404


def test_port_put_delete_port(api_client, sample_switch1, sample_port1):

    r = api_client.delete(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      sample_port1.id))
    assert r.status_code == 204


def test_port_put_delete_non_existant_port(api_client,
                                           sample_switch1):

    r = api_client.delete(
        "{}/switch/{}/port/{}".format(base_url,
                                      sample_switch1.id,
                                      4242))
    assert r.status_code == 404
