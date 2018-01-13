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
    parsed_mac = urllib.parse.quote_plus(device_bonnet["mac"])
    r = api_client.put(base_url + "/device/" + parsed_mac,
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 201


def test_device_update(api_client):
    parsed_mac = urllib.parse.quote_plus(device_bonnet["mac"])
    r = api_client.put(base_url + "/device/" + parsed_mac,
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 204


def test_device_get(api_client):
    mac = urllib.parse.quote_plus("non_existent_MAC")
    r = api_client.get(''.join([base_url, "/device/", mac]))
    assert r.status_code == 404


def test_device_delete(api_client):
    parsed_mac = urllib.parse.quote_plus(device_bonnet["mac"])
    r = api_client.delete(base_url + "/device/" + parsed_mac)
    assert r.status_code == 204


def test_device_unexistant_delete(api_client):
    mac = urllib.parse.quote_plus("non_existent_MAC")
    r = api_client.delete(base_url + "/device/" + mac)
    assert r.status_code == 404


def test_device_filter(api_client):
    parsed_mac_bonnet = urllib.parse.quote_plus(device_bonnet["mac"])
    r = api_client.put(base_url + "/device/" + parsed_mac_bonnet,
                       data=json.dumps(device_bonnet),
                       content_type='application/json')
    assert r.status_code == 201

    parsed_mac_cazal = urllib.parse.quote_plus(device_cazal["mac"])
    r = api_client.put(base_url + "/device/" + parsed_mac_cazal,
                       data=json.dumps(device_cazal),
                       content_type='application/json')
    assert r.status_code == 201
    r = api_client.get(base_url+"/device/?username="+device_cazal["username"])
    assert r.status_code == 200
    response = json.loads(r.data)
    assert len(response) == 1
