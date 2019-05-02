from dataclasses import asdict
from pytest import fixture, raises
from unittest.mock import MagicMock

from src.entity.room import Room
from src.exceptions import RoomNotFound, VLANNotFound, RoomNumberMismatchError, MissingRequiredFieldError, \
    InvalidVLANNumber, IntMustBePositiveException
from src.use_case.interface.room_repository import RoomRepository
from src.use_case.room_manager import RoomManager, MutationRequest
from src.use_case.util.mutation import Mutation


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_room_repository: RoomRepository,
                        sample_room: Room,
                        room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        result, count = room_manager.search(ctx, limit=1, offset=2, terms='terms')

        assert [sample_room] == result
        assert 1 == count
        mock_room_repository.search_room_by.assert_called_once_with(ctx, limit=1, offset=2, terms='terms')

    def test_invalid_offset(self,
                            ctx,
                            mock_room_repository: RoomRepository,
                            sample_room: Room,
                            room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        with raises(IntMustBePositiveException):
            room_manager.search(ctx, offset=-1)

    def test_invalid_limit(self,
                           ctx,
                           mock_room_repository: RoomRepository,
                           sample_room: Room,
                           room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        with raises(IntMustBePositiveException):
            room_manager.search(ctx, limit=-1)


class TestGetByNumber:
    def test_happy_path(self,
                        ctx,
                        mock_room_repository: RoomRepository,
                        sample_room: Room,
                        room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        result = room_manager.get_by_number(ctx, '1234')

        assert sample_room == result
        mock_room_repository.search_room_by.assert_called_once()

    def test_not_found(self,
                       ctx,
                       mock_room_repository: RoomRepository,
                       room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([], 0))
        with raises(RoomNotFound):
            room_manager.get_by_number(ctx, '1234')

        mock_room_repository.search_room_by.assert_called_once()


class TestUpdateOrCreate:
    @fixture
    def mutation_request(self):
        return MutationRequest(
            room_number='1234',
            description='desc',
            phone_number='phone',
            vlan_number='vlan',
        )

    def test_create_happy_path(self,
                               ctx,
                               mock_room_repository: RoomRepository,
                               sample_room: Room,
                               mutation_request: MutationRequest,
                               room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([], 0))
        created = room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)

        assert created is True
        mock_room_repository.create_room(ctx, **asdict(mutation_request))

    def test_create_room_number_mismatch(self,
                                         ctx,
                                         mock_room_repository: RoomRepository,
                                         sample_room: Room,
                                         mutation_request: MutationRequest,
                                         room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([], 0))
        mutation_request.room_number = 'something different than the other room number'
        with raises(RoomNumberMismatchError):
            room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)

    def test_create_vlan_not_found(self,
                                   ctx,
                                   mock_room_repository: RoomRepository,
                                   mutation_request: MutationRequest,
                                   sample_room: Room,
                                   room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([], 0))
        mock_room_repository.create_room = MagicMock(side_effect=InvalidVLANNumber)
        with raises(VLANNotFound):
            room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)

    def test_update_happy_path(self,
                               ctx,
                               mock_room_repository: RoomRepository,
                               sample_room: Room,
                               mutation_request: MutationRequest,
                               room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        created = room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)

        assert created is False
        mock_room_repository.update_room(ctx, sample_room.room_number, **asdict(mutation_request))

    def test_update_vlan_not_found(self,
                                   ctx,
                                   mock_room_repository: RoomRepository,
                                   sample_room: Room,
                                   mutation_request: MutationRequest,
                                   room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        mock_room_repository.update_room = MagicMock(side_effect=InvalidVLANNumber)
        with raises(VLANNotFound):
            room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)

    def test_update_missing_room_number(self,
                                        ctx,
                                        mutation_request: MutationRequest,
                                        sample_room: Room,
                                        room_manager: RoomManager):
        mock_room_repository.search_room_by = MagicMock(return_value=([sample_room], 1))
        mutation_request.room_number = Mutation.NOT_SET

        with raises(MissingRequiredFieldError):
            room_manager.update_or_create(ctx, sample_room.room_number, mutation_request)


class TestDelete:
    def test_happy_path(self,
                        ctx,
                        mock_room_repository: RoomRepository,
                        room_manager: RoomManager):
        mock_room_repository.delete_room = MagicMock()
        room_manager.delete(ctx, '1234')

        mock_room_repository.delete_room.assert_called_once_with(ctx, room_number='1234')

    def test_not_found(self,
                       ctx,
                       mock_room_repository: RoomRepository,
                       room_manager: RoomManager):
        mock_room_repository.delete_room = MagicMock(side_effect=RoomNotFound)
        with raises(RoomNotFound):
            room_manager.delete(ctx, '1234')


@fixture
def room_manager(mock_room_repository):
    return RoomManager(
        room_repository=mock_room_repository
    )


@fixture
def mock_room_repository():
    return MagicMock(spec=RoomRepository)
