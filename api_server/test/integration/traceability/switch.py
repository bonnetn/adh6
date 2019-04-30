# coding=utf-8
import logging

from test.integration.resource import logs_contains
from test.integration.test_switch import test_switch_post_valid, test_switch_update_existant_switch, \
    test_switch_delete_existant_switch


def test_switch_log_create(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_post_valid(api_client)

    log = 'TestingClient created a switch'
    assert logs_contains(caplog, log)


def test_switch_log_update(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_update_existant_switch(api_client)

    log = 'TestingClient updated the switch 1'
    assert logs_contains(caplog, log)


def test_switch_log_delete(api_client, caplog):
    with caplog.at_level(logging.INFO):
        test_switch_delete_existant_switch(api_client)

    log = 'TestingClient deleted the switch 1'
    assert logs_contains(caplog, log)
