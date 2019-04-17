import pytest

from CONFIGURATION import TEST_DATABASE as db_settings
from adh.auth import authenticate_temp_account, token_info
from adh.interface_adapter.sql.model.database import Database as db
from .context import app


@pytest.fixture
def api_client(sample_naina, sample_naina_expired):
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        s = db.get_db().get_session()

        s.add(sample_naina_expired)
        s.add(sample_naina)
        s.commit()

        yield c


def test_authenticate_temp_account_unknown(api_client):
    with app.app.test_request_context():
        assert authenticate_temp_account("UNKNOWN_TOKEN") is None


def test_authenticate_temp_account_expired(api_client, sample_naina_expired):
    with app.app.test_request_context():
        assert authenticate_temp_account(sample_naina_expired.access_token) is None


def test_authenticate_temp_account_success(api_client, sample_naina):
    with app.app.test_request_context():
        assert authenticate_temp_account(sample_naina.access_token) == {
            'uid': 'TEMP_ACCOUNT(2)[Nain Ha]',
            'scope': ['profile'],
            'groups': ['adh6_user']
        }


def test_token_info_testing(api_client):
    with app.app.test_request_context():
        assert token_info("IGNORED") == {'uid': 'TestingClient', 'scope': ['profile'], 'groups': []}


def test_token_info_naina(api_client, sample_naina):
    with app.app.test_request_context():
        assert token_info("NAINA_{}".format(sample_naina.access_token)) == {
            'uid': 'TEMP_ACCOUNT(2)[Nain Ha]',
            'groups': ['adh6_user'],
            'scope': ['profile']
        }
