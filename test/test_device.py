import json

import pytest
from adh.model.database import Database as db
from adh.settings.unit_test_settings import DATABASE as db_settings
from adh.model.models import Ordinateur, Portable, Adherent

from .resource import base_url, INVALID_MAC


@pytest.fixture
def sample_member():
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='a',
    )


@pytest.fixture
def sample_member2():
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        password='b',
    )


@pytest.fixture
def sample_wired_device(sample_member):
    return Ordinateur(
        mac='96:24:F6:D0:48:A7',
        ip='157.159.42.42',
        dns='bonnet_n4651',
        adherent=sample_member,
        ipv6='e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4'
    )


@pytest.fixture
def sample_wireless_device(sample_member2):
    return Portable(
        mac='80:65:F3:FC:44:A9',
        adherent=sample_member2,
    )


'''
Device that will be inserted/updated when tests are run.
It is not present in the api_client by default
'''
TEST_WIRELESS_DEVICE = {
  'mac': '01:23:45:67:89:AC',
  'ipAddress': '127.0.0.1',
  'ipv6Address': 'c69f:6c5:754c:d301:df05:ba81:76a8:ddc4',
  'connectionType': 'wireless',
  'username': 'dubois_j'
}

TEST_WIRED_DEVICE = {
  'mac': '01:23:45:67:89:AD',
  'ipAddress': '127.0.0.1',
  'ipv6Address': 'dbb1:39b7:1e8f:1a2a:3737:9721:5d16:166',
  'connectionType': 'wired',
  'username': 'dubois_j'
}


def prep_db(session,
            sample_member,
            sample_member2,
            sample_wired_device,
            sample_wireless_device):
    session.add_all([
        sample_member,
        sample_member2,
        sample_wired_device,
        sample_wireless_device
    ])
    session.commit()


@pytest.fixture
def api_client(sample_member,
               sample_member2,
               sample_wired_device,
               sample_wireless_device):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_member,
                sample_member2,
                sample_wired_device,
                sample_wireless_device)
        yield c


def test_device_to_dict(sample_wired_device):
    dict(sample_wired_device)


def test_device_filter_all_devices(api_client):
    r = api_client.get('{}/device/'.format(base_url))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 2


@pytest.mark.parametrize('user,expected', [
    ('reignier', 1),
    ('dubois_j', 1),
    ('gates_bi', 0),  # Non existant user
    ('dubois', 0),    # Exact match
])
def test_device_filter_wired_by_username(
        api_client, user, expected):
    r = api_client.get('{}/device/?username={}'.format(
        base_url,
        user
    ))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == expected


@pytest.mark.parametrize('terms,expected', [
    ('96:24:F6:D0:48:A7', 1),   # Should find sample wired device
    ('96:', 1),
    ('e91f', 1),
    ('157.159', 1),
    ('80:65:F3:FC:44:A9', 1),  # Should find sample wireless device
    ('F3:FC', 1),
    (':', 2),                  # Should find everything
    ('00:', 0),                # Should find nothing
])
def test_device_filter_by_terms(
        api_client, sample_wired_device, terms, expected):
    r = api_client.get('{}/device/?terms={}'.format(
        base_url,
        terms,
    ))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == expected


def test_device_filter_hit_limit(api_client, sample_member):
    s = db.get_db().get_session()
    LIMIT = 10

    # Create a lot of devices
    for i in range(LIMIT*2):
        suffix = "{0:04X}".format(i)
        dev = Portable(
            adherent=sample_member,
            mac='00:00:00:00:'+suffix[:2]+":"+suffix[2:]
        )
        s.add(dev)
    s.commit()

    r = api_client.get('{}/device/?limit={}'.format(base_url, LIMIT))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == LIMIT


def test_device_put_create_wireless(api_client):
    ''' Can create a valid wireless device ? '''
    r = api_client.put('{}/device/{}'.format(base_url,
                                             TEST_WIRELESS_DEVICE['mac']),
                       data=json.dumps(TEST_WIRELESS_DEVICE),
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
    dev['mac'] = test_mac
    r = api_client.put('{}/device/{}'.format(base_url, dev['mac']),
                       data=json.dumps(dev),
                       content_type='application/json')
    assert r.status_code == 400 or r.status_code == 405


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
        data=json.dumps(TEST_WIRELESS_DEVICE),
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


def test_device_get_unknown_mac(api_client):
    mac = '00:00:00:00:00:00'
    r = api_client.get('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 404


def test_device_get_valid_wired(api_client, sample_wired_device):
    mac = sample_wired_device.mac
    r = api_client.get('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_device_get_valid_wireless(api_client, sample_wireless_device):
    mac = sample_wireless_device.mac
    r = api_client.get('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_device_delete_wired(api_client, sample_wired_device):
    mac = sample_wired_device.mac
    r = api_client.delete('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 204

    s = db.get_db().get_session()
    q = s.query(Ordinateur)
    q = q.filter(Ordinateur.mac == mac)
    assert not s.query(q.exists()).scalar(), "Object not actually deleted"


def test_device_delete_wireless(api_client, sample_wireless_device):
    mac = sample_wireless_device.mac
    r = api_client.delete('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 204

    s = db.get_db().get_session()
    q = s.query(Portable)
    q = q.filter(Portable.mac == mac)
    assert not s.query(q.exists()).scalar(), "Object not actually deleted"


def test_device_delete_unexistant(api_client):
    mac = '00:00:00:00:00:00'
    r = api_client.delete('{}/device/{}'.format(base_url, mac))
    assert r.status_code == 404
