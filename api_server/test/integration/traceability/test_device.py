import logging
import pytest

from config.TEST_CONFIGURATION import DATABASE
from src.interface_adapter.http_api.auth import TESTING_CLIENT
from src.interface_adapter.sql.model.database import Database as db
from test.integration.resource import logs_contains
from test.integration.test_device import test_device_put_create_wired, test_device_put_create_wireless, \
    test_device_put_update_wired, test_device_put_update_wireless, test_device_delete_wired, test_device_delete_wireless


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
    from ..context import app
    with app.app.test_client() as c:
        db.init_db(DATABASE, testing=True)
        prep_db(db.get_db().get_session(),
                wired_device,
                wireless_device,
                sample_member3)
        yield c


def test_device_log_create_wired(api_client, caplog, wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wired(api_client, wired_device_dict)

    assert logs_contains(caplog,
                         'device_create',
                         admin=TESTING_CLIENT,
                         mac=wired_device_dict['mac'])


def test_device_log_create_wireless(api_client, caplog, wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wireless(api_client, wireless_device_dict)

    assert logs_contains(caplog,
                         'device_create',
                         admin=TESTING_CLIENT,
                         mac=wireless_device_dict['mac'])


def test_device_log_update_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wired(api_client, wired_device,
                                     wired_device_dict)

    assert logs_contains(caplog,
                         'device_update',
                         admin=TESTING_CLIENT,
                         mac='96-24-F6-D0-48-A7')


def test_device_log_update_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wireless(api_client, wireless_device,
                                        wireless_device_dict)

    assert logs_contains(caplog,
                         'device_update',
                         admin=TESTING_CLIENT,
                         mac='80-65-F3-FC-44-A9')


def test_device_log_delete_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wired(api_client, wired_device)

    assert logs_contains(caplog,
                         'device_delete',
                         admin=TESTING_CLIENT,
                         mac='96-24-F6-D0-48-A7')


def test_device_log_delete_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wireless(api_client, wireless_device)

    assert logs_contains(caplog,
                         'device_delete',
                         admin=TESTING_CLIENT,
                         mac='80-65-F3-FC-44-A9')
