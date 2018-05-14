import json
import pytest
from adh.model.database import Database as db
from CONFIGURATION import TEST_DATABASE as db_settings
from test.resource import base_url
from adh.model.models import Adherent, Chambre, Vlan


@pytest.fixture
def sample_vlan():
    yield Vlan(
        numero=42,
        adresses="192.168.42.1",
        adressesv6="fe80::1",
    )


@pytest.fixture
def sample_room(sample_vlan):
    yield Chambre(
        numero=1234,
        description='chambre 1',
        vlan=sample_vlan,
    )


@pytest.fixture
def sample_room2(sample_vlan):
    yield Chambre(
        numero=1111,
        description='chambre 2',
        vlan=sample_vlan,
    )


@pytest.fixture
def sample_member(sample_room):
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='a',
        chambre=sample_room,
    )


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
def sample_member3(sample_room2):
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
            sample_member, sample_member2, sample_member3,
            sample_room, sample_room2, sample_vlan):
    session.add_all([
        sample_room, sample_room2,
        sample_member, sample_member2, sample_member3])
    session.commit()


@pytest.fixture
def api_client(sample_member, sample_member2, sample_member3,
               sample_room, sample_room2, sample_vlan):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_member,
                sample_member2,
                sample_member3,
                sample_room,
                sample_room2,
                sample_vlan)
        yield c


def test_user_to_dict(sample_member):
    dict(sample_member)


def test_user_filter_all(api_client):
    r = api_client.get('{}/user/'.format(base_url))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 3


def test_user_filter_all_with_invalid_limit(api_client):
    r = api_client.get('{}/user/?limit={}'.format(base_url, -1))
    assert r.status_code == 400


def test_user_filter_all_with_limit(api_client):
    r = api_client.get('{}/user/?limit={}'.format(base_url, 1))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_by_room_number(api_client):
    r = api_client.get('{}/user/?roomNumber={}'.format(base_url, 1234))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_by_non_existant_room_number(api_client):
    r = api_client.get('{}/user/?roomNumber={}'.format(base_url, 6666))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 0


def test_user_filter_terms_first_name(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "Jean"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_terms_last_name(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "ubois"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_terms_email(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "bgdu78"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_terms_login(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "dubois_j"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_terms_comment(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "routeur"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_filter_terms_nonexistant(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "azerty"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 0


def test_user_filter_terms_test_upper_case(api_client):
    r = api_client.get('{}/user/?terms={}'.format(base_url, "DUBOIS_J"))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1


def test_user_get_existant(api_client):
    r = api_client.get('{}/user/{}'.format(base_url, "dubois_j"))
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_user_get_nonexistant(api_client):
    r = api_client.get('{}/user/{}'.format(base_url, "bond_jam"))
    assert r.status_code == 404


def test_user_delete_existant(api_client):
    r = api_client.delete('{}/user/{}'.format(base_url, "dubois_j"))
    assert r.status_code == 204

    s = db.get_db().get_session()
    q = s.query(Adherent)
    q = q.filter(Adherent.login == "dubois_j")
    assert not s.query(q.exists()).scalar()


def test_user_delete_non_existant(api_client):
    r = api_client.delete('{}/user/{}'.format(base_url, "azerty"))
    assert r.status_code == 404


def test_user_put_user_create_invalid_email(api_client):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "roomNumber": 1111,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "INVALID_EMAIL",
        "username": "doe_john"
    }
    res = api_client.put(
        '{}/user/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json')
    assert res.status_code == 400


def test_user_put_user_create_unknown_room(api_client):
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
        '{}/user/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json')
    assert res.status_code == 400


def test_user_put_user_create(api_client):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "roomNumber": 1111,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "john.doe@gmail.com",
        "username": "doe_john"
    }
    res = api_client.put(
        '{}/user/{}'.format(base_url, ["username"]),
        data=json.dumps(body),
        content_type='application/json')
    assert res.status_code == 201


def test_user_put_user_update(api_client):
    body = {
        "firstName": "Jean-Louis",
        "lastName": "Dubois",
        "roomNumber": 1111,
        "comment": "comment",
        "departureDate": "2000-01-23T04:56:07.000+00:00",
        "associationMode": "2000-01-23T04:56:07.000+00:00",
        "email": "john.doe@gmail.com",
        "username": "dubois_j"
    }
    res = api_client.put(
        '{}/user/{}'.format(base_url, body["username"]),
        data=json.dumps(body),
        content_type='application/json')
    assert res.status_code == 204


def test_user_post_add_membership_not_found(api_client):
    body = {
      "duration": 365,
      "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/user/{}/membership'.format(base_url, "charlie"),
        data=json.dumps(body),
        content_type='application/json')
    assert result.status_code == 404


def test_user_post_add_membership_ok(api_client):
    body = {
      "duration": 365,
      "start": "2000-01-23T04:56:07.000+00:00"
    }
    result = api_client.post(
        '{}/user/{}/membership'.format(base_url, "dubois_j"),
        data=json.dumps(body),
        content_type='application/json')
    assert result.status_code == 200
