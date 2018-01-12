import json
import urllib.parse

import pytest

from .resource import base_url, device_bonnet, device_cazal


@pytest.fixture
def api_client():
    from .context import app
    with app.app.test_client() as c:
        yield c


def test_device_list(api_client):
    r = api_client.get(base_url + "/device/")
    assert r.status_code == 200
    response = json.loads(r.data)
    assert len(response) == 2


def test_device_insert(api_client):
    r = api_client.put(base_url + "/device/" + urllib.parse.quote_plus(device_bonnet["mac"]),
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 201


def test_device_update(api_client):
    r = api_client.put(base_url + "/device/" + urllib.parse.quote_plus(device_bonnet["mac"]),
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 204


def test_device_get(api_client):
    r = api_client.get(base_url + "/device/" + urllib.parse.quote_plus("non_existent_MAC"))
    assert r.status_code == 404


def test_device_delete(api_client):
    r = api_client.delete(base_url + "/device/" + urllib.parse.quote_plus(device_bonnet["mac"]))
    assert r.status_code == 204


def test_device_unexistant_delete(api_client):
    r = api_client.delete(base_url + "/device/" + urllib.parse.quote_plus("non_existent_MAC"))
    assert r.status_code == 404


def test_device_filter(api_client):
    r = api_client.put(base_url + "/device/" + urllib.parse.quote_plus(device_bonnet["mac"]),
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 201
    r = api_client.put(base_url + "/device/" + urllib.parse.quote_plus(device_cazal["mac"]),
                       data=json.dumps(device_cazal),
                       content_type='application/json')
    assert r.status_code == 201
    r = api_client.get(base_url + "/device/?username=" + device_cazal["username"])
    assert r.status_code == 200
    response = json.loads(r.data)
    assert len(response) == 1
