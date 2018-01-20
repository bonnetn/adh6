import json
import urllib.parse

import pytest
from model.database import Database as db
from unit_test_settings import DATABASE as db_settings
from model.models import Ordinateur, Portable, Adherent

from .resource import base_url, INVALID_MAC


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
def sample_wired_device(sample_member):
    return Ordinateur(
        mac='12:34:56:78:9A:BC',
        ip='157.159.42.42',
        dns='bonnet_n4651',
        adherent=sample_member,
        ipv6='e91f:e45a:0db3:15df:a4a7:6316:d8d7:1d4a'
    )


@pytest.fixture
def sample_wireless_device(sample_member):
    return Portable(
        mac='12:34:56:78:9A:FF',
        adherent=sample_member,
    )


'''
Device that will be inserted/updated when tests are run.
It is not present in the api_client by default
'''
TEST_WIRELESS_DEVICE = {
  'mac': '01:23:45:67:89:AC',
  'ipAddress': '127.0.0.1',
  'ipv6Address': 'string',
  'connectionType': 'wireless',
  'username': 'dubois_j'
}

TEST_WIRED_DEVICE = {
  'mac': '01:23:45:67:89:AD',
  'ipAddress': '127.0.0.1',
  'ipv6Address': 'string',
  'connectionType': 'wired',
  'username': 'dubois_j'
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
        db.init_db(db_settings, testing=True)
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


def test_device_put_create_wireless(api_client):
    ''' Can create a valid wireless device ? '''
    r = api_client.put('{}/device/{}'.format(base_url,
                                             TEST_WIRED_DEVICE['mac']),
                       data=json.dumps(TEST_WIRED_DEVICE),
                       content_type='application/json')
    assert r.status_code == 201


def test_device_put_create_wired(api_client):
    ''' Can create a valid wired device ? '''
    r = api_client.put('{}/device/{}'.format(base_url,
                                             TEST_WIRED_DEVICE['mac']),
                       data=json.dumps(TEST_WIRED_DEVICE),
                       content_type='application/json')
    assert r.status_code == 201


@pytest.mark.parametrize('test_mac', INVALID_MAC)
def test_device_put_create_invalid_mac_address(api_client, test_mac):
    ''' Create with invalid mac address '''
    dev = dict(TEST_WIRED_DEVICE)
    dev['macAddress'] = test_mac
    r = api_client.put('{}/device/{}'.format(base_url, dev['mac']),
                       data=json.dumps(dev),
                       content_type='application/json')
    assert r.status_code == 400


def test_device_put_create_invalid_username(api_client):
    ''' Create with invalid mac address '''
    dev = dict(TEST_WIRED_DEVICE)
    dev['username'] = 'abcdefgh'
    r = api_client.put('{}/device/{}'.format(base_url, dev['mac']),
                       data=json.dumps(dev),
                       content_type='application/json')
    assert r.status_code == 400


def test_device_put_update_wireless(api_client, sample_wireless_device):
    ''' Can update a valid wireless device ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wireless_device.mac),
        data=json.dumps(TEST_WIRELESS_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_put_update_wired(api_client, sample_wired_device):
    ''' Can update a valid wired device ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wired_device.mac),
        data=json.dumps(TEST_WIRED_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_put_update_wired_to_wireless(api_client, sample_wired_device):
    ''' Can update a valid wired device and cast it into a wireless d ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wired_device.mac),
        data=json.dumps(TEST_WIRED_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_put_update_wireless_to_wired(api_client,
                                             sample_wireless_device):
    ''' Can update a valid wireless device and cast it into a wired d ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wireless_device.mac),
        data=json.dumps(TEST_WIRED_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_put_update_wired_and_wireless_to_wireless(api_client,
                                                          sample_wired_device):
    '''
    Test if the controller is able to handle the case where the MAC address is
    in the Wireless table _AND_ the Wired table
    Tests the case where we want to move the mac to the wireless table
    '''
    # Add a wireless device that has the same mac as SAMPLE_WIRED_DEVICE
    dev_with_same_mac = Portable(
        mac=sample_wired_device.mac,
        adherent_id=1,
    )
    session = db.get_db().get_session()
    session.add(dev_with_same_mac)
    session.commit()

    # Then try to update it...
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wired_device.mac),
        data=json.dumps(TEST_WIRELESS_DEVICE),
        content_type='application/json')
    assert r.status_code == 204


def test_device_put_update_wired_and_wireless_to_wired(api_client,
                                                       sample_wireless_device):
    '''
    Test if the controller is able to handle the case where the MAC address is
    in the Wireless table _AND_ the Wired table
    Tests the case where we want to move the mac to the wired table
    '''
    # Add a wired device that has the same mac as SAMPLE_WIRELESS_DEVICE
    dev_with_same_mac = Ordinateur(
        mac=sample_wireless_device.mac,
        adherent_id=1,
    )
    session = db.get_db().get_session()
    session.add(dev_with_same_mac)
    session.commit()

    # Then try to update it...
    r = api_client.put(
        '{}/device/{}'.format(base_url, sample_wireless_device.mac),
        data=json.dumps(TEST_WIRED_DEVICE),
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
