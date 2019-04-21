import logging

from test.integration.resource import logs_contains
from test.integration.test_member import test_member_put_member_create, test_member_put_member_update, \
    test_member_delete_existant, test_member_change_password_ok, test_member_post_add_membership_ok, \
    test_member_get_logs


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
