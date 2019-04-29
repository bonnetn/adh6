import logging
import pytest

from config.TEST_CONFIGURATION import DATABASE as db_settings
from src.interface_adapter.http_api.auth import TESTING_CLIENT
from src.interface_adapter.sql.model.database import Database as db
from test.integration.resource import logs_contains
from test.integration.test_port import test_port_post_create_port, test_port_put_update_port, test_port_delete_port


def prep_db(session,
            sample_port1,
            sample_port2,
            sample_room1):
    session.add_all([
        sample_port1,
        sample_port2,
        sample_room1,
    ])
    session.commit()


@pytest.fixture
def api_client(sample_port1, sample_port2, sample_room1):
    from ..context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_port1,
                sample_port2,
                sample_room1)
        yield c


def test_port_log_create_port(api_client, sample_switch1, caplog):
    with caplog.at_level(logging.INFO):
        test_port_post_create_port(api_client, sample_switch1)

    assert logs_contains(caplog,
                         'port_create',
                         admin=TESTING_CLIENT)


def test_port_log_update_port(api_client, sample_switch1,
                              sample_port1, caplog):
    with caplog.at_level(logging.INFO):
        test_port_put_update_port(api_client, sample_switch1, sample_port1)

    assert logs_contains(caplog,
                         'port_update',
                         admin=TESTING_CLIENT)


def test_port_log_delete_port(api_client, sample_switch1,
                              sample_port1, caplog):
    with caplog.at_level(logging.INFO):
        test_port_delete_port(api_client, sample_switch1, sample_port1)

    assert logs_contains(caplog,
                         'port_delete',
                         admin=TESTING_CLIENT,
                         port_id=sample_port1.id)
