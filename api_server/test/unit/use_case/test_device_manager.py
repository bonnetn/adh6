# coding=utf-8 import datetime import datetime import datetime
from pytest import fixture, raises
from unittest.mock import MagicMock

from src.entity.device import Device, DeviceType
from src.entity.member import Member
from src.entity.room import Room
from src.use_case.device_manager import DeviceManager
from src.use_case.exceptions import IntMustBePositiveException, MemberNotFound
from src.use_case.interface.device_repository import DeviceRepository
from src.use_case.interface.ip_allocator import IPAllocator
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.room_repository import RoomRepository
from test.unit.use_case.conftest import TEST_USERNAME, TEST_MAC_ADDRESS1


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_device_repository: MagicMock,
                        sample_device: Device,
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


class TestUpdateOrCreate:
    def test_create_happy_path(self,
                               ctx,
                               mock_device_repository: MagicMock,
                               mock_member_repository: MagicMock,
                               mock_room_repository: MagicMock,
                               mock_ip_allocator: MagicMock,
                               sample_member: Member,
                               sample_room: Room,
                               device_manager: DeviceManager):
        ipv4 = '192.0.0.1'
        ipv6 = 'fe80::1'
        # Given...

        # That the owner exists:
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # That the device does not exist in the DB:
        mock_device_repository.search_device_by = MagicMock(return_value=([], 0))

        # That the owner has a room (needed to get the ip range to allocate the IP):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        mock_ip_allocator.allocate_ip_v4 = MagicMock(return_value=ipv4)
        mock_ip_allocator.allocate_ip_v6 = MagicMock(return_value=ipv6)

        # When...
        created = device_manager.update_or_create(ctx, mac_address=TEST_MAC_ADDRESS1,
                                                  owner_username=TEST_USERNAME, connection_type=DeviceType.Wired)

        # Expect...
        assert created is True
        mock_device_repository.create_device.assert_called_once_with(ctx, mac_address=TEST_MAC_ADDRESS1,
                                                                     owner_username=TEST_USERNAME,
                                                                     connection_type=DeviceType.Wired,
                                                                     ip_v4_address=ipv4,
                                                                     ip_v6_address=ipv6)

    def test_update_happy_path(self,
                               ctx,
                               mock_device_repository: MagicMock,
                               mock_member_repository: MagicMock,
                               sample_member: Member,
                               sample_device: Device,
                               device_manager: DeviceManager):
        # Given...

        # That the owner exists:
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # That the device exists in the DB:
        mock_device_repository.search_device_by = MagicMock(return_value=([sample_device], 1))

        # When...
        created = device_manager.update_or_create(ctx, mac_address=sample_device.mac_address,
                                                  owner_username=TEST_USERNAME, connection_type=DeviceType.Wireless)

        # Expect...
        assert created is False
        mock_device_repository.update_device.assert_called_once_with(ctx, mac_address=sample_device.mac_address,
                                                                     owner_username=TEST_USERNAME,
                                                                     connection_type=DeviceType.Wireless,
                                                                     ip_v4_address=None,
                                                                     ip_v6_address=None)

    def test_invalid_owner_username(self,
                                    ctx,
                                    mock_member_repository: MagicMock,
                                    mock_device_repository: MagicMock,
                                    device_manager: DeviceManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([], 0))

        # When...
        with raises(MemberNotFound):
            device_manager.update_or_create(ctx, mac_address=TEST_MAC_ADDRESS1,
                                            owner_username='', connection_type=DeviceType.Wired)

        # Expect...
        mock_device_repository.create_device.assert_not_called()
        mock_device_repository.update_device.assert_not_called()


@fixture
def device_manager(
        mock_device_repository: DeviceRepository,
        mock_member_repository: MemberRepository,
        mock_room_repository: RoomRepository,
        mock_ip_allocator: IPAllocator,
):
    return DeviceManager(
        device_storage=mock_device_repository,
        member_storage=mock_member_repository,
        room_storage=mock_room_repository,
        ip_allocator=mock_ip_allocator,
    )


@fixture
def mock_ip_allocator():
    return MagicMock(spec=IPAllocator)


@fixture
def mock_member_repository():
    return MagicMock(spec=MemberRepository)


@fixture
def mock_room_repository():
    return MagicMock(spec=RoomRepository)


@fixture
def mock_device_repository():
    return MagicMock(spec=DeviceRepository)
