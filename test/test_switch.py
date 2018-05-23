import pytest
import json
from .resource import base_url
from CONFIGURATION import TEST_DATABASE as db_settings
from adh.model.models import Switch
from adh.model.database import Database as db
from .resource import INVALID_IP, TEST_HEADERS


@pytest.fixture
def sample_switch():
    yield Switch(
        id=1,
        description='Switch',
        ip='192.168.102.2',
        communaute='communaute',
    )


def prep_db(session, sample_switch):
    """ Insert the test objects in the db """
    session.add(sample_switch)
    session.commit()  # TODO: remove?


@pytest.fixture
def api_client(sample_switch):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(), sample_switch)
        yield c


def assert_switch_in_db(body):
    s = db.get_db().get_session()
    q = s.query(Switch)
    q = q.filter(Switch.ip == body["ip"])
    sw = q.one()
    assert sw.ip == body["ip"]
    assert sw.communaute == body["community"]
    assert sw.description == body["description"]


def test_switch_to_dict(sample_switch):
    dict_sw = {
        'id': 1,
        'ip': '192.168.102.2',
        'community': 'communaute',
        'description': 'Switch'
    }

    assert dict(sample_switch) == dict_sw


@pytest.mark.parametrize("test_ip", INVALID_IP)
def test_switch_post_invalid_ip(api_client, test_ip):
    sample_switch = {
      "description": "Test Switch",
      "ip": test_ip,
      "community": "myGreatCommunity"
    }
    r = api_client.post(
        "{}/switch/".format(base_url),
        data=json.dumps(sample_switch),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 400


def test_switch_post_valid(api_client):

    sample_switch = {
      "description": "Test Switch",
      "ip": "192.168.103.128",
      "community": "myGreatCommunity"
    }

    # Insert data to the database
    r = api_client.post(
        "{}/switch/".format(base_url),
        data=json.dumps(sample_switch),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 201
    assert 'Location' in r.headers
    assert r.headers['Location'] == 'http://localhost/switch/2'
    assert_switch_in_db(sample_switch)


def test_switch_get_all_invalid_limit(api_client):
    r = api_client.get(
        "{}/switch/?limit={}".format(base_url, -1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


def test_switch_get_all_limit(api_client):
    r = api_client.get(
        "{}/switch/?limit={}".format(base_url, 0),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    t = json.loads(r.data.decode('utf-8'))
    assert len(t) == 0


def test_switch_get_all(api_client):
    r = api_client.get(
        "{}/switch/".format(base_url),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    t = json.loads(r.data.decode('utf-8'))
    assert t
    assert len(t) == 1


def test_switch_get_existant_switch(api_client):
    r = api_client.get(
        "{}/switch/{}".format(base_url, 1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_switch_get_non_existant_switch(api_client):
    r = api_client.get(
        "{}/switch/{}".format(base_url, 100000),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 404


def test_switch_filter_by_term_ip(api_client):
    terms = "102.2"
    r = api_client.get(
        "{}/switch/?terms={}".format(base_url, terms),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    result = json.loads(r.data.decode('utf-8'))
    assert result
    assert len(result) == 1


def test_switch_filter_by_term_desc(api_client):
    terms = "Switch"
    r = api_client.get(
        "{}/switch/?terms={}".format(base_url, terms),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    result = json.loads(r.data.decode('utf-8'))
    assert result
    assert len(result) == 1


def test_switch_filter_by_term_nonexistant(api_client):
    terms = "HEYO"
    r = api_client.get(
        "{}/switch/?terms={}".format(base_url, terms),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    result = json.loads(r.data.decode('utf-8'))
    assert not result


@pytest.mark.parametrize("test_ip", INVALID_IP)
def test_switch_update_switch_invalid_ip(api_client, test_ip):
    sample_switch = {
      "description": "Modified switch",
      "ip": test_ip,
      "community": "communityModified"
    }

    r = api_client.put(
        "{}/switch/{}".format(base_url, 1),
        data=json.dumps(sample_switch),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 400


def test_switch_update_existant_switch(api_client):
    sample_switch = {
      "description": "Modified switch",
      "ip": "192.168.103.132",
      "community": "communityModified"
    }

    r = api_client.put(
        "{}/switch/{}".format(base_url, 1),
        data=json.dumps(sample_switch),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 204
    assert_switch_in_db(sample_switch)


def test_switch_update_non_existant_switch(api_client):
    sample_switch = {
      "description": "Modified switch",
      "ip": "192.168.103.132",
      "community": "communityModified"
    }

    r = api_client.put(
        "{}/switch/{}".format(base_url, 100000),
        data=json.dumps(sample_switch),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 404


def test_switch_delete_existant_switch(api_client):
    r = api_client.delete(
        "{}/switch/{}".format(base_url, 1),
        headers=TEST_HEADERS
    )
    assert r.status_code == 204
    s = db.get_db().get_session()
    q = s.query(Switch)
    q = q.filter(Switch.id == 1)

    assert not s.query(q.exists()).scalar()


def test_switch_delete_non_existant_switch(api_client):
    r = api_client.delete(
        "{}/switch/{}".format(base_url, 10000),
        headers=TEST_HEADERS
    )
    assert r.status_code == 404
