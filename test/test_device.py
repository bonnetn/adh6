import json
import urllib.parse

import pytest
from model.database import Database as db
from unit_test_settings import DATABASE as db_settings
from model.models import Ordinateur, Portable

from .resource import base_url, device_bonnet, device_cazal


def prep_db(session):
    sample_wired_device = Ordinateur(
        mac="12:34:56:78:9A:BC",
        ip="157.159.42.42",
        dns='bonnet_n4651',
        adherent_id=12,  # TODO transform this attribute into a foreign keyword
        ipv6='e91f:e45a:0db3:15df:a4a7:6316:d8d7:1d4a'
    )
    sample_wireless_device = Portable(
        mac="12:34:56:78:9A:FF",
        adherent_id=12,  # TODO transform this attribute into a foreign keyword
    )
    session.add_all([sample_wired_device, sample_wireless_device])
    session.commit()


@pytest.fixture
def api_client():
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings)
        prep_db(db.get_db().get_session())
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
