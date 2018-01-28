import json
import pytest
from model.database import Database as db
from unit_test_settings import DATABASE as db_settings
from test.resource import base_url
from model.models import Adherent


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
def sample_member2():
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        password='',
    )


def prep_db(session, sample_member, sample_member2):
    session.add_all([sample_member, sample_member2])
    session.commit()


@pytest.fixture
def api_client(sample_member, sample_member2):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_member,
                sample_member2)
        yield c


def test_user_filter_all(api_client):
    r = api_client.get('{}/user/'.format(base_url))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 2


def test_user_filter_all_with_limit(api_client):
    r = api_client.get('{}/user/?limit={}'.format(base_url, 1))
    assert r.status_code == 200

    response = json.loads(r.data.decode('utf-8'))
    assert len(response) == 1
