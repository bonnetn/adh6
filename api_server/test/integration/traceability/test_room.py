import logging

from src.interface_adapter.http_api.auth import TESTING_CLIENT
from test.integration.resource import logs_contains
from test.integration.test_room import test_room_put_new_room, test_room_put_update_room, test_room_delete_existant_room


def test_room_log_create_room(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_room_put_new_room(api_client)

    assert logs_contains(caplog,
                         'room_create',
                         admin=TESTING_CLIENT,
                         room_number=5111)


def test_room_log_update_room(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_room_put_update_room(api_client)

    assert logs_contains(caplog,
                         'room_update',
                         admin=TESTING_CLIENT,
                         room_number=5110)


def test_room_log_delete_room(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_room_delete_existant_room(api_client)

    assert logs_contains(caplog,
                         'room_delete',
                         admin=TESTING_CLIENT,
                         room_number=5110)
