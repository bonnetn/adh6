import datetime
import json
import logging

import pytest
from dateutil import parser

from CONFIGURATION import TEST_DATABASE as db_settings, PRICES
from adh.interface_adapter.sql.model.database import Database as db
from adh.interface_adapter.sql.model.models import Adherent
from adh.util.hash import ntlm_hash
from test.integration.resource import (
    base_url, TEST_HEADERS, assert_modification_was_created,
    logs_contains)


@pytest.fixture
def sample_member2(sample_room2):
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        commentaires='Desauthent pour routeur',
        password='a',
        chambre=sample_room2,
    )


@pytest.fixture
def sample_member13(sample_room2):
    """ Membre sans chambre """
    yield Adherent(
        nom='Robert',
        prenom='Dupond',
        mail='robi@hotmail.fr',
        login='dupond_r',
        commentaires='a',
        password='a',
    )


def prep_db(session,
            sample_member1, sample_member2, sample_member13,
            wired_device, wireless_device,
            sample_room1, sample_room2, sample_vlan):
    session.add_all([
        sample_room1, sample_room2,
        wired_device, wireless_device,
        sample_member1, sample_member2, sample_member13])
    session.commit()


@pytest.fixture
def api_client(sample_member1, sample_member2, sample_member13,
               wired_device, wireless_device,
               sample_room1, sample_room2, sample_vlan):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_member1,
                sample_member2,
                sample_member13,
                wired_device,
                wireless_device,
                sample_room1,
                sample_room2,
                sample_vlan)
        yield c


def assert_member_in_db(body):
    # Actually check that the object was inserted
    s = db.get_db().get_session()
    q = s.query(Adherent)
    q = q.filter(Adherent.login == body["username"])
    r = q.one()
    assert r.nom == body["lastName"]
    assert r.prenom == body["firstName"]
    assert r.mail == body["email"]
    assert r.date_de_depart == parser.parse(body["departureDate"]).date()
    asso_time = parser.parse(body["associationMode"]).replace(tzinfo=None)
    assert r.mode_association == asso_time
    assert r.chambre.numero == body["roomNumber"]
    assert r.commentaires == body["comment"]
    assert r.login == body["username"]


def test_member_to_dict(sample_member1):
    t = datetime.datetime(2011, 4, 30, 17, 50, 17)
    dict_member = {'email': 'j.dubois@free.fr',
                   'firstName': 'Jean-Louis',
                   'lastName': 'Dubois',
                   'username': 'dubois_j',
                   'roomNumber': 5110,
                   'departureDate': datetime.datetime(2005, 7, 14, 12, 30)}

    assert dict(sample_member1) == dict_member


def test_member_filter_all(api_client):
    r = api_client.get(
        '{}/member/'.format(base_url),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 3


def test_member_filter_all_with_invalid_limit(api_client):
    r = api_client.get(
        '{}/member/?limit={}'.format(base_url, -1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


def test_member_filter_all_with_limit(api_client):
    r = api_client.get(
        '{}/member/?limit={}'.format(base_url, 1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_by_roomNumber(api_client):
    r = api_client.get(
        '{}/member/?roomNumber={}'.format(base_url, 5110),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_by_non_existant_roomNumber(api_client):
    r = api_client.get(
        '{}/member/?roomNumber={}'.format(base_url, 6666),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 0


def test_member_filter_terms_first_name(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "Jean"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_terms_last_name(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "ubois"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_terms_email(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "bgdu78"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_terms_login(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "dubois_j"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_terms_comment(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "routeur"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_filter_terms_nonexistant(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "azerty"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 0


def test_member_filter_terms_test_upper_case(api_client):
    r = api_client.get(
        '{}/member/?terms={}'.format(base_url, "DUBOIS_J"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_member_get_existant(api_client):
    r = api_client.get(
        '{}/member/{}'.format(base_url, "dubois_j"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_member_get_nonexistant(api_client):
    r = api_client.get(
        '{}/member/{}'.format(base_url, "bond_jam"),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 404


def test_member_delete_existant(api_client):
    r = api_client.delete(
        '{}/member/{}'.format(base_url, "dubois_j"),
        headers=TEST_HEADERS
    )
    assert r.status_code == 204
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Adherent)
    q = q.filter(Adherent.login == "dubois_j")
    assert not s.query(q.exists()).scalar()


def test_member_delete_non_existant(api_client):
    r = api_client.delete(
        '{}/member/{}'.format(base_url, "azerty"),
        headers=TEST_HEADERS
    )
    assert r.status_code == 404


def test_member_put_member_create_invalid_email(api_client):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "roomNumber": 4592,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "INVALID_EMAIL",
        "username": "doe_john"
    }
    res = api_client.put(
        '{}/member/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 400


def test_member_put_member_create_unknown_room(api_client):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "roomNumber": 9999,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "john.doe@gmail.com",
        "username": "doe_john"
    }
    res = api_client.put(
        '{}/member/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert 400 == res.status_code


def test_member_put_member_create(api_client):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "roomNumber": 4592,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "john.doe@gmail.com",
        "username": "doe_john"
    }
    res = api_client.put(
        '{}/member/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert 201 == res.status_code
    assert_modification_was_created(db.get_db().get_session())

    assert_member_in_db(body)


def test_member_patch_username(api_client):
    body = {
        "username": "TEST",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "TEST"
    })


def test_member_patch_email(api_client):
    body = {
        "email": "TEST@TEST.FR",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "TEST@TEST.FR",
        "username": "dubois_j"
    })


def test_member_patch_associationmode(api_client):
    body = {
        "associationMode": "1996-01-01T00:00:00",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "1996-01-01T00:00:00",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })


def test_member_patch_departuredate(api_client):
    body = {
        "departureDate": "1996-01-01",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": "1996-01-01",
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })

def test_member_patch_comment(api_client):
    body = {
        "comment": "TEST",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": "TEST",
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })


def test_member_patch_roomnumber(api_client):
    body = {
        "roomNumber": 4592,
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 4592,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })


def test_member_patch_lastname(api_client):
    body = {
        "lastName": "TEST",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "Jean-Louis",
        "lastName": "TEST",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })


def test_member_patch_firstname(api_client):
    body = {
        "firstName": "TEST",
    }
    res = api_client.patch(
        '{}/member/{}'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())
    assert_member_in_db({
        "firstName": "TEST",
        "lastName": "Dubois",
        "roomNumber": 5110,
        "comment": None,
        "departureDate": str(datetime.datetime(2005, 7, 14, 12, 30)),
        "associationMode": "2011-04-30T17:50:17",
        "email": "j.dubois@free.fr",
        "username": "dubois_j"
    })


def test_member_post_add_membership_not_found(api_client):
    body = {
        "duration": 31,
        "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/member/{}/membership'.format(base_url, "charlie"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 404


def test_member_put_member_update(api_client):
    body = {
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 4592,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "john.doe@gmail.com",
        "username": "dubois_j"
    }
    res = api_client.put(
        '{}/member/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert res.status_code == 204
    assert_modification_was_created(db.get_db().get_session())

    assert_member_in_db(body)


def test_member_post_add_membership_not_found(api_client):
    body = {
        "duration": list(PRICES.keys())[0],
        "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/member/{}/membership/'.format(base_url, "charlie"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 404


def test_member_post_add_membership_undefined_price(api_client):
    '''
    Add a membership record for a duration that does not exist in the price
    chart
    '''
    body = {
        "duration": 1337,
        "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/member/{}/membership/'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 400


def test_member_post_add_membership_ok(api_client):
    body = {
        "duration": 360,
        "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/member/{}/membership/'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 200
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Adherent)
    q = q.filter(Adherent.login == "dubois_j")
    assert q.one().date_de_depart == datetime.date(2001, 1, 17)


def test_member_change_password_ok(api_client):
    USERNAME = "dubois_j"
    body = {
        "password": "on;X\\${QG55Bd\"#NyL#+k:_xEdJrEDT7",
    }
    result = api_client.put(
        '{}/member/{}/password/'.format(base_url, USERNAME),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 204
    assert_modification_was_created(db.get_db().get_session())

    s = db.get_db().get_session()
    q = s.query(Adherent)
    q = q.filter(Adherent.login == USERNAME)
    r = q.one()
    assert r.password == ntlm_hash(body["password"])


def test_member_change_password_member_not_exist(api_client):
    body = {
        "password": "on;X\\${QG55Bd\"#NyL#+k:_xEdJrEDT7",
    }
    result = api_client.put(
        '{}/member/{}/password/'.format(base_url, "sherlock"),
        data=json.dumps(body),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 404


def test_member_get_logs(api_client):
    USERNAME = "dubois_j"
    result = api_client.get(
        '{}/member/{}/logs/'.format(base_url, USERNAME),
        content_type='application/json',
        headers=TEST_HEADERS,
    )
    assert result.status_code == 200
    assert json.loads(result.data.decode('utf-8')) == ["test_log"]


def test_member_log_create(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_put_member_create(api_client)

    log = 'TestingClient created the member doe_john'
    assert logs_contains(caplog, log)


def test_member_log_update(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_put_member_update(api_client)

    log = 'TestingClient updated the member dubois_j'
    assert logs_contains(caplog, log)


def test_member_log_delete(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_delete_existant(api_client)

    log = 'TestingClient deleted the member dubois_j'
    assert logs_contains(caplog, log)


def test_member_log_add_membership(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_post_add_membership_ok(api_client)

    log = 'TestingClient created a membership record for dubois_j of 360 days starting from 2000-01-23T04:56:07+00:00'
    assert logs_contains(caplog, log)


def test_member_log_update_password(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_change_password_ok(api_client)

    log = 'TestingClient updated the password of dubois_j'
    assert logs_contains(caplog, log)


def test_member_log_get_logs(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_get_logs(api_client)

    log = 'TestingClient fetched the logs of dubois_j'
    assert logs_contains(caplog, log)
