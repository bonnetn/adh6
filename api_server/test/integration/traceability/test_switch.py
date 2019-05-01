# coding=utf-8
import logging
import pytest

from config.TEST_CONFIGURATION import DATABASE as db_settings
from src.interface_adapter.http_api.auth import TESTING_CLIENT
from src.interface_adapter.sql.model.database import Database as db
from test.integration.resource import logs_contains
from test.integration.test_switch import test_switch_post_valid, test_switch_update_existant_switch, \
    test_switch_delete_existant_switch


@pytest.fixture
def sample_switch():
    yield Switch(
        id=1,
        description='Switch',
        ip='192.168.102.2',
        communaute='communaute',
    )


def prep_db(session, sample_switch1):
    """ Insert the test objects in the Db """
    session.add(sample_switch1)
    session.commit()


@pytest.fixture
def api_client(sample_switch1):
    from ..context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(), sample_switch1)
        yield c


def test_switch_log_create(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_post_valid(api_client)

    log = 'TestingClient created a switch'
    assert logs_contains(caplog, 'switch_create',
                         admin=TESTING_CLIENT)


def test_switch_log_update(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_update_existant_switch(api_client)

    assert logs_contains(caplog, 'switch_update',
                         admin=TESTING_CLIENT,
                         switch_id=1)


def test_switch_log_delete(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_delete_existant_switch(api_client)

    assert logs_contains(caplog, 'switch_delete',
                         admin=TESTING_CLIENT,
                         switch_id=1)
