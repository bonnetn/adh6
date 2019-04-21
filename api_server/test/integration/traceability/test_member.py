import logging

from src.interface_adapter.http_api.auth import TESTING_CLIENT
from test.integration.resource import logs_contains
from test.integration.test_member import test_member_put_member_create, test_member_put_member_update, \
    test_member_delete_existant, test_member_change_password_ok, test_member_post_add_membership_ok, \
    test_member_get_logs


def test_member_log_create(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_put_member_create(api_client)

    assert logs_contains(
        caplog,
        'member_create',
        admin=TESTING_CLIENT,
        username='doe_john',
    )


def test_member_log_update(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_put_member_update(api_client)

    assert logs_contains(
        caplog,
        'member_whole_update',
        admin=TESTING_CLIENT,
        username='dubois_j',
    )


def test_member_log_delete(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_delete_existant(api_client)

    assert logs_contains(
        caplog,
        'member_delete',
        admin=TESTING_CLIENT,
        username='dubois_j',
    )


def test_member_log_add_membership(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_post_add_membership_ok(api_client)

    assert logs_contains(
        caplog,
        'create_membership_record',
        admin=TESTING_CLIENT,
        username='dubois_j',
        duration_in_days=360,
        start_date='2000-01-23T04:56:07+00:00',
    )


def test_member_log_update_password(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_change_password_ok(api_client)

    assert logs_contains(
        caplog,
        'member_password_update',
        admin=TESTING_CLIENT,
        username='dubois_j',
    )


def test_member_log_get_logs(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_member_get_logs(api_client)

    assert logs_contains(
        caplog,
        'member_get_logs',
        admin=TESTING_CLIENT,
        username='dubois_j',
    )
