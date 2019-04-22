import logging

from test.integration.resource import logs_contains
from test.integration.test_device import test_device_put_create_wired, test_device_put_create_wireless, \
    test_device_put_update_wired, test_device_put_update_wireless, test_device_delete_wired, test_device_delete_wireless


def test_device_log_create_wired(api_client, caplog, wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wired(api_client, wired_device_dict)

    log = 'TestingClient created the device 01-23-45-67-89-AD'
    assert logs_contains(caplog, log)
    assert logs_contains(caplog, 'wired')


def test_device_log_create_wireless(api_client, caplog, wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_create_wireless(api_client, wireless_device_dict)

    log = 'TestingClient created the device 01-23-45-67-89-AC'
    assert logs_contains(caplog, log)
    assert logs_contains(caplog, 'wireless')


def test_device_log_update_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wired(api_client, wired_device,
                                     wired_device_dict)

    log = 'TestingClient updated the device 96-24-F6-D0-48-A7'
    assert logs_contains(caplog, log)
    assert logs_contains(caplog, 'wired')


def test_device_log_update_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_put_update_wireless(api_client, wireless_device,
                                        wireless_device_dict)

    log = 'TestingClient updated the device 80-65-F3-FC-44-A9'
    assert logs_contains(caplog, log)
    assert logs_contains(caplog, 'wireless')


def test_device_log_delete_wired(api_client, caplog, wired_device,
                                 wired_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wired(api_client, wired_device)

    log = 'TestingClient deleted the device 96-24-F6-D0-48-A7'
    assert logs_contains(caplog, log)


def test_device_log_delete_wireless(api_client, caplog, wireless_device,
                                    wireless_device_dict):
    with caplog.at_level(logging.INFO):
        test_device_delete_wireless(api_client, wireless_device)

    log = 'TestingClient deleted the device 80-65-F3-FC-44-A9'
    assert logs_contains(caplog, log)
