import json
import logging

import pytest

from CONFIGURATION import TEST_DATABASE as db_settings
from adh.model.database import Database as db
from adh.model.models import Ordinateur, Portable
from .resource import (
    base_url, INVALID_MAC, INVALID_IP, INVALID_IPv6, TEST_HEADERS,
    assert_modification_was_created
)


def prep_db(session,
            wired_device,
            wireless_device,
            sample_member3):
    session.add_all([
        wired_device,
        wireless_device,
        sample_member3,
    ])
    session.commit()


@pytest.fixture
def api_client(wired_device,
               wireless_device,
               sample_member3):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                wired_device,
                wireless_device,
                sample_member3)
        yield c


def test_device_filter_all_devices(api_client):
    r = api_client.get(
        '{}/device/'.format(base_url),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 2


@pytest.mark.parametrize('user,expected', [
    ('reignier', 1),
    ('dubois_j', 1),
    ('gates_bi', 0),  # Non existant user
    ('dubois', 0),  # Exact match
])
def test_device_filter_wired_by_username(
        api_client, user, expected):
    r = api_client.get(
        '{}/device/?username={}'.format(
            base_url,
            user
        ),
        headers=TEST_HEADERS
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == expected


@pytest.mark.parametrize('terms,expected', [
    ('96-24-F6-D0-48-A7', 1),  # Should find sample wired device
    ('96-', 1),
    ('e91f', 1),
    ('157.159', 1),
    ('80-65-F3-FC-44-A9', 1),  # Should find sample wireless device
    ('F3-FC', 1),
    ('-', 2),  # Should find everything
    ('00-', 0),  # Should find nothing
])
def test_device_filter_by_terms(
        api_client, wired_device, terms, expected):
    r = api_client.get(
        '{}/device/?terms={}'.format(
            base_url,
            terms,
        ),
        headers=TEST_HEADERS
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == expected


def test_device_filter_invalid_limit(api_client):
    r = api_client.get(
        '{}/device/?limit={}'.format(base_url, -1),
        headers=TEST_HEADERS
    )
    assert r.status_code == 400


def test_device_filter_hit_limit(api_client, sample_member1):
    s = db.get_db().get_session()
    LIMIT = 10

    # Create a lot of devices
    for i in range(LIMIT * 2):
        suffix = "{0:04X}".format(i)
        dev = Portable(
            adherent=sample_member1,
            mac='00-00-00-00-' + suffix[:2] + "-" + suffix[2:]
        )
        s.add(dev)
    s.commit()

    r = api_client.get(
        '{}/device/?limit={}'.format(base_url, LIMIT),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == LIMIT


def test_device_put_create_wireless(api_client, wireless_device_dict):
    ''' Can create a valid wireless device ? '''
    addr = '{}/device/{}'.format(base_url, wireless_device_dict['mac'])
    r = api_client.put(addr,
                       data=json.dumps(wireless_device_dict),
                       content_type='application/json',
                       headers=TEST_HEADERS)
    assert r.status_code == 201
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_create_wired_without_ip(api_client, wired_device_dict):
    '''
    Can create a valid wired device? Create two devices and check the IP
    '''

    del wired_device_dict['ipAddress']
    del wired_device_dict['ipv6Address']
    r = api_client.put('{}/device/{}'.format(base_url,
                                             wired_device_dict['mac']),
                       data=json.dumps(wired_device_dict),
                       content_type='application/json',
                       headers=TEST_HEADERS)
    assert r.status_code == 201
    assert_modification_was_created(db.get_db().get_session())

    wired_device_dict["mac"] = "AB-CD-EF-01-23-45"
    r = api_client.put('{}/device/{}'.format(base_url,
                                             wired_device_dict['mac']),
                       data=json.dumps(wired_device_dict),
                       content_type='application/json',
                       headers=TEST_HEADERS)
    assert r.status_code == 201
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Ordinateur)
    q = q.filter(Ordinateur.mac == wired_device_dict["mac"])
    dev = q.one()
    assert dev.ip == "192.168.42.3"
    assert dev.ipv6 == 'fe80::3'


def test_device_put_create_wired(api_client, wired_device_dict):
    ''' Can create a valid wired device ? '''
    r = api_client.put('{}/device/{}'.format(base_url,
                                             wired_device_dict['mac']),
                       data=json.dumps(wired_device_dict),
                       content_type='application/json',
                       headers=TEST_HEADERS)
    assert r.status_code == 201
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Ordinateur)
    q = q.filter(Ordinateur.mac == wired_device_dict["mac"])
    dev = q.one()
    assert dev.ip == "127.0.0.1"


def test_device_put_create_different_mac_addresses(api_client,
                                                   wired_device_dict):
    ''' Create with invalid mac address '''
    wired_device_dict['mac'] = "11-11-11-11-11-11"
    r = api_client.put('{}/device/{}'.format(base_url, "22-22-22-22-22-22"),
                       data=json.dumps(wired_device_dict),
                       content_type='application/json',
                       headers=TEST_HEADERS)
    assert r.status_code == 400


@pytest.mark.parametrize('test_mac', INVALID_MAC)
def test_device_put_create_invalid_mac_address(api_client,
                                               test_mac,
                                               wired_device_dict):
    ''' Create with invalid mac address '''
    wired_device_dict['mac'] = test_mac
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device_dict['mac']),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400 or r.status_code == 405


@pytest.mark.parametrize('test_ip', INVALID_IPv6)
def test_device_put_create_invalid_ipv6(api_client, test_ip,
                                        wired_device_dict):
    ''' Create with invalid ip address '''
    wired_device_dict['ipv6Address'] = test_ip
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device_dict['mac']),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


@pytest.mark.parametrize('test_ip', INVALID_IP)
def test_device_put_create_invalid_ipv4(api_client, test_ip,
                                        wired_device_dict):
    ''' Create with invalid ip address '''
    wired_device_dict['ipAddress'] = test_ip
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device_dict['mac']),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


def test_device_put_create_invalid_username(api_client, wired_device_dict):
    ''' Create with invalid mac address '''
    wired_device_dict['username'] = 'abcdefgh'
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device_dict['mac']),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


def test_device_put_update_wireless(api_client, wireless_device,
                                    wireless_device_dict):
    ''' Can update a valid wireless device ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, wireless_device.mac),
        data=json.dumps(wireless_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_update_wired(api_client, wired_device, wired_device_dict):
    ''' Can update a valid wired device ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device.mac),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_update_wired_to_wireless(api_client, wired_device,
                                             wireless_device_dict):
    ''' Can update a valid wired device and cast it into a wireless d ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device.mac),
        data=json.dumps(wireless_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_update_wireless_to_wired(api_client,
                                             wireless_device,
                                             wired_device_dict):
    ''' Can update a valid wireless device and cast it into a wired d ? '''
    r = api_client.put(
        '{}/device/{}'.format(base_url, wireless_device.mac),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_update_wired_and_wireless_to_wireless(
        api_client,
        wired_device,
        wireless_device_dict):
    '''
    Test if the controller is able to handle the case where the MAC address is
    in the Wireless table _AND_ the Wired table
    Tests the case where we want to move the mac to the wireless table
    '''
    # Add a wireless device that has the same mac as WIRED_DEVICE
    dev_with_same_mac = Portable(
        mac=wired_device.mac,
        adherent_id=1,
    )
    s = db.get_db().get_session()
    s.add(dev_with_same_mac)
    s.commit()

    # Then try to update it...
    r = api_client.put(
        '{}/device/{}'.format(base_url, wired_device.mac),
        data=json.dumps(wireless_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_put_update_wired_and_wireless_to_wired(api_client,
                                                       wireless_device,
                                                       wired_device_dict):
    '''
    Test if the controller is able to handle the case where the MAC address is
    in the Wireless table _AND_ the Wired table
    Tests the case where we want to move the mac to the wired table
    '''
    # Add a wired device that has the same mac as WIRELESS_DEVICE
    dev_with_same_mac = Ordinateur(
        mac=wireless_device.mac,
        adherent_id=1,
    )
    s = db.get_db().get_session()
    s.add(dev_with_same_mac)
    s.commit()

    # Then try to update it...
    r = api_client.put(
        '{}/device/{}'.format(base_url, wireless_device.mac),
        data=json.dumps(wired_device_dict),
        content_type='application/json',
        headers=TEST_HEADERS)
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())


def test_device_get_unknown_mac(api_client):
    mac = '00-00-00-00-00-00'
    r = api_client.get(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 404


def test_device_get_valid_wired(api_client, wired_device):
    mac = wired_device.mac
    r = api_client.get(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_device_get_valid_wireless(api_client, wireless_device):
    mac = wireless_device.mac
    r = api_client.get(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_device_delete_wired(api_client, wired_device):
    mac = wired_device.mac
    r = api_client.delete(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Ordinateur)
    q = q.filter(Ordinateur.mac == mac)
    assert not s.query(q.exists()).scalar(), "Object not actually deleted"


def test_device_delete_wireless(api_client, wireless_device):
    mac = wireless_device.mac
    r = api_client.delete(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Portable)
    q = q.filter(Portable.mac == mac)
    assert not s.query(q.exists()).scalar(), "Object not actually deleted"


def test_device_delete_unexistant(api_client):
    mac = '00-00-00-00-00-00'
    r = api_client.delete(
        '{}/device/{}'.format(base_url, mac),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 404


def test_device_log_create_wired(api_client, caplog, wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wired(api_client, wired_device_dict)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient created the device 01-23-45-67-89-AD\n{"connectionType": '
        '"wired", "ipAddress": "127.0.0.1", "ipv6Address": '
        '"dbb1:39b7:1e8f:1a2a:3737:9721:5d16:166", "mac": "01-23-45-67-89-AD", '
        '"username": "dupontje"}'
    )


def test_device_log_create_wireless(api_client, caplog, wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wireless(api_client, wireless_device_dict)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient created the device 01-23-45-67-89-AC\n{"'
        'connectionType": "wireless", "mac": "01-23-45-67-89-AC", "'
        'username": "dubois_j"}'
    )


def test_device_log_update_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wired(api_client, wired_device,
                                     wired_device_dict)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient updated the device 96-24-F6-D0-48-A7\n{"connectionType"'
        ': "wired", "ipAddress": "127.0.0.1", "ipv6Address": '
        '"dbb1:39b7:1e8f:1a2a:3737:9721:5d16:166", "mac": "01-23-45-67-89-AD",'
        ' "username": "dupontje"}'
    )


def test_device_log_update_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wireless(api_client, wireless_device,
                                        wireless_device_dict)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient updated the device 80-65-F3-FC-44-A9\n{"'
        'connectionType": "wireless", "mac": "01-23-45-67-89-AC", "'
        'username": "dubois_j"}'
    )


def test_device_log_delete_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wired(api_client, wired_device)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient deleted the device 96-24-F6-D0-48-A7'
    )


def test_device_log_delete_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wireless(api_client, wireless_device)

    assert caplog.record_tuples[1] == (
        'root', 20,
        'TestingClient deleted the device 80-65-F3-FC-44-A9'
    )
