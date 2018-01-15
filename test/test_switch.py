import pytest
import json
from .resource import base_url


@pytest.fixture
def api_client():
    from .context import app
    with app.app.test_client() as c:
        yield c


def test_valid_switch_insert(api_client):

    sample_switch = {
      "description": "Test Switch",
      "ip": "192.168.103.128",
      "community": "myGreatCommunity"
    }

    # Insert data to the database
    r = api_client.post("{}/switch/".format(base_url),
                        data=json.dumps(sample_switch),
                        content_type='application/json')
    assert r.status_code == 201
    assert 'Location' in r.headers

    # Make sure the data is now fetchable
    r = api_client.get(r.headers["Location"])
    assert r.status_code == 200, "Couldn't fetch the newly created switch"
    assert json.loads(r.data)


def test_switch_get_all(api_client):
    r = api_client.get("{}/switch/".format(base_url))
    assert r.status_code == 200
    assert json.loads(r.data)


def test_switch_get_existant_switch(api_client):
    r = api_client.get("{}/switch/{}".format(base_url, 1))
    assert r.status_code == 200
    assert json.loads(r.data)


def test_switch_get_non_existant_switch(api_client):
    r = api_client.get("{}/switch/{}".format(base_url, 100000))
    assert r.status_code == 404


def test_switch_update_existant_switch(api_client):
    sample_switch = {
      "description": "Modified switch",
      "ip": "192.168.103.132",
      "community": "communityModified"
    }

    r = api_client.put("{}/switch/{}".format(base_url, 1),
                       data=json.dumps(sample_switch),
                       content_type='application/json')
    assert r.status_code == 204

    r = api_client.get("{}/switch/{}".format(base_url, 1))
    assert r.status_code == 200
    assert json.loads(r.data) == sample_switch, "The switch wasn't modified"


def test_switch_update_non_existant_switch(api_client):
    sample_switch = {
      "description": "Modified switch",
      "ip": "192.168.103.132",
      "community": "communityModified"
    }

    r = api_client.put("{}/switch/{}".format(base_url, 100000),
                       data=json.dumps(sample_switch),
                       content_type='application/json')
    assert r.status_code == 404


def test_switch_delete_existant_switch(api_client):
    r = api_client.delete("{}/switch/{}".format(base_url, 1))
    assert r.status_code == 204

    r = api_client.get("{}/switch/{}".format(base_url, 1))
    assert r.status_code == 404


def test_switch_delete_non_existant_switch(api_client):
    r = api_client.delete("{}/switch/{}".format(base_url, 10000))
    assert r.status_code == 404
