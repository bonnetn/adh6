# coding=utf-8 import datetime import datetime import datetime
from pytest import fixture, raises
from unittest.mock import MagicMock

from src.entity.device import DeviceInfo, DeviceType
from src.use_case.device_manager import DeviceManager
from src.use_case.exceptions import IntMustBePositiveException
from src.use_case.interface.device_repository import DeviceRepository
from test.unit.use_case.conftest import TEST_USERNAME


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_device_repository: MagicMock,
                        sample_device: DeviceInfo,
                        device_manager: DeviceManager):
        # Given...
        terms = 'blah blah blah'
        mock_device_repository.search_device_by = MagicMock(return_value=([sample_device], 1))

        # When...
        result, count = device_manager.search(ctx, limit=10, offset=1, username=TEST_USERNAME, terms=terms)

        # Expect...
        assert [sample_device] == result
        assert 1 == count
        mock_device_repository.search_device_by.assert_called_once_with(ctx, limit=10, offset=1, username=TEST_USERNAME,
                                                                        terms=terms)

    def test_invalid_offset(self,
                            ctx,
                            device_manager: DeviceManager):
        # When...
        with raises(IntMustBePositiveException):
            device_manager.search(ctx, limit=1, offset=-1, username=TEST_USERNAME, terms='blabla')

    def test_invalid_limit(self,
                           ctx,
                           device_manager: DeviceManager):
        # When...
        with raises(IntMustBePositiveException):
            device_manager.search(ctx, limit=-1, offset=1, username=TEST_USERNAME, terms='blabla')


@fixture
def device_manager(
        mock_device_repository: DeviceRepository,
):
    return DeviceManager(
        device_storage=mock_device_repository,
    )


@fixture
def mock_device_repository():
    return MagicMock(spec=DeviceRepository)


@fixture
def sample_device():
    return DeviceInfo(
        mac='FF:FF:FF:FF:FF:FF',
        owner_username=TEST_USERNAME,
        connection_type=DeviceType.Wired,
        ip_address='127.0.0.1',
        ipv6_address='127.0.0.1',
    )
