import json
import urllib.parse

import pytest
from model.database import Database as db
from unit_test_settings import DATABASE as db_settings
from model.models import Ordinateur, Portable, Adherent

from .resource import base_url


@pytest.fixture
def sample_member():
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='',
    )


@pytest.fixture
def sample_wired_device():
    return Ordinateur(
        mac='12:34:56:78:9A:BC',
        ip='157.159.42.42',
        dns='bonnet_n4651',
        adherent_id=1,
        ipv6='e91f:e45a:0db3:15df:a4a7:6316:d8d7:1d4a'
    )


@pytest.fixture
def sample_wireless_device():
    return Portable(
        mac='12:34:56:78:9A:FF',
        adherent_id=1,
    )


'''
Device that will be inserted/updated when tests are run.
It is not present in the api_client by default
'''
TEST_DEVICE = {
  'mac': '01:23:45:67:89:AB',
  'ipAddress': '127.0.0.1',
  'ipv6Address': 'string',
  'connectionType': 'wired',
  'username': 'doe_john'
}


def prep_db(session,
            sample_member,
            sample_wired_device,
            sample_wireless_device):
    session.add_all([
        sample_member,
        sample_wired_device,
        sample_wireless_device
    ])
    session.commit()


@pytest.fixture
def api_client(sample_member, sample_wired_device, sample_wireless_device):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings)
        prep_db(db.get_db().get_session(),
                sample_member,
                sample_wired_device,
                sample_wireless_device)
        yield c


def test_device_list(api_client):
    r = api_client.get(base_url + '/device/')
    assert r.status_code == 200
    response = json.loads(r.data)
    assert len(response) == 2


def test_device_insert(api_client):
    r = api_client.put('{}/device/{}'.format(base_url, TEST_DEVICE['mac']),
                       data=json.dumps(TEST_DEVICE),
                       content_type='application/json')
    assert r.status_code == 201


def test_device_update(api_client):
    r = api_client.put(
        '{}/device/{}'.format(base_url, SAMPLE_WIRED_DEVICE['mac']),
        data=json.dumps(TEST_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_get(api_client):
    mac = urllib.parse.quote_plus('non_existent_MAC')
    r = api_client.get(''.join([base_url, '/device/', mac]))
    assert r.status_code == 404


def test_device_delete(api_client, sample_wired_device):
    parsed_mac = urllib.parse.quote_plus(sample_wired_device['mac'])
    r = api_client.delete(base_url + '/device/' + parsed_mac)
    assert r.status_code == 204


def test_device_unexistant_delete(api_client):
    mac = urllib.parse.quote_plus('non_existent_MAC')
    r = api_client.delete(base_url + '/device/' + mac)
    assert r.status_code == 404


def test_device_filter(api_client, sample_wired_device):
    r = api_client.get(
        base_url+'/device/?username='+sample_wired_device.adherent.login)
    assert r.status_code == 200
    response = json.loads(r.data)
    assert len(response) == 1
