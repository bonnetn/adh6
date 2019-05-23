import datetime
import json
from dateutil import parser

import pytest

from config.TEST_CONFIGURATION import DATABASE as db_settings
from src.interface_adapter.sql.model.database import Database as db
from src.interface_adapter.sql.model.models import Transaction, PaymentMethod, Account, AccountType
from test.integration.resource import TEST_HEADERS, INVALID_TRANSACTION_VALUE, base_url


@pytest.fixture
def sample_payment_method():
    return PaymentMethod(
            id=1,
            name='liquide'
        )


@pytest.fixture
def sample_account1():
    return Account(
        id='1',
        name='test1',
        actif=True,
        creation_date=datetime.datetime(2005, 7, 14, 12, 30),
        account_type=AccountType(
            id=1,
            name='adherent'
        ))


@pytest.fixture
def sample_account2():
    return Account(
        id='2',
        name='test3',
        actif=True,
        creation_date=datetime.datetime(2005, 7, 14, 12, 31),
        account_type=AccountType(
            id=2,
            name='event'
        ))


@pytest.fixture
def sample_transaction(sample_account1, sample_account2, sample_payment_method):
    return Transaction(
        src_account=sample_account1,
        dst_account=sample_account2,
        name='description',
        value='200',
        attachments='',
        timestamp=datetime.datetime(2005, 7, 14, 12, 30),
        payment_method=sample_payment_method)


def prep_db(session, sample_transaction):
    """ Insert the test objects in the Db """
    session.add(sample_transaction)
    session.commit()


@pytest.fixture
def api_client(sample_transaction):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(), sample_transaction)
        yield c


def assert_transaction_in_db(body):
    s = db.get_db().get_session()
    q = s.query(Transaction)
    q = q.filter(Transaction.name == body["name"])
    sw = q.one()
    assert sw.name == body["name"]
    assert sw.src == body["src"]
    assert sw.dst == body["dst"]
    assert sw.value == body["value"]


@pytest.mark.parametrize("test_value", INVALID_TRANSACTION_VALUE)
def test_switch_post_invalid_value(api_client, test_value):
    sample_transaction1 = {
        "src": 1,
        "dst": 2,
        "name": "test",
        "attachments": "",
        "value": test_value,
        "payment_method": "liquide"
    }
    r = api_client.post(
        "{}/transaction/".format(base_url),
        data=json.dumps(sample_transaction1),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 400


def test_transaction_post_valid(api_client):
    sample_transaction1 = {
        "src": 1,
        "dst": 2,
        "name": "test",
        "attachments": "",
        "value": 400,
        "payment_method": '1'
    }

    # Insert data to the database
    r = api_client.post(
        "{}/transaction/".format(base_url),
        data=json.dumps(sample_transaction1),
        content_type='application/json',
        headers=TEST_HEADERS
    )
    assert r.status_code == 201
    assert_transaction_in_db(sample_transaction1)


def test_transaction_get_all_invalid_limit(api_client):
    r = api_client.get(
        "{}/transaction/?limit={}".format(base_url, -1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 400


def test_transaction_get_all_limit(api_client):
    r = api_client.get(
        "{}/transaction/?limit={}".format(base_url, 0),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    t = json.loads(r.data.decode('utf-8'))
    assert len(t) == 0


def test_transaction_get_all(api_client):
    r = api_client.get(
        "{}/transaction/".format(base_url),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    t = json.loads(r.data.decode('utf-8'))
    assert t
    assert len(t) == 1


def test_transaction_get_existant_transaction(api_client):
    r = api_client.get(
        "{}/transaction/{}".format(base_url, 1),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    assert json.loads(r.data.decode('utf-8'))


def test_transaction_get_non_existant_transaction(api_client):
    r = api_client.get(
        "{}/transaction/{}".format(base_url, 100000),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 404


def test_transaction_filter_by_term_desc(api_client):
    terms = "descri"
    r = api_client.get(
        "{}/transaction/?terms={}".format(base_url, terms),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    result = json.loads(r.data.decode('utf-8'))
    assert result
    assert len(result) == 1


def test_transaction_filter_by_term_nonexistant(api_client):
    terms = "BONJOUR?"
    r = api_client.get(
        "{}/transaction/?terms={}".format(base_url, terms),
        headers=TEST_HEADERS,
    )
    assert r.status_code == 200
    result = json.loads(r.data.decode('utf-8'))
    assert not result

