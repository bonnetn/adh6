from dataclasses import asdict
from pytest import fixture, raises
from unittest.mock import MagicMock

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.port import Port
from src.exceptions import SwitchNotFound, RoomNotFound, PortNotFound, InvalidRoomNumber, InvalidSwitchID, \
    IntMustBePositiveException
from src.use_case.interface.port_repository import PortRepository
from src.use_case.port_manager import PortManager, MutationRequest


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_port_repository: PortRepository,
                        sample_port: Port,
                        port_manager: PortManager):
        mock_port_repository.search_port_by = MagicMock(return_value=([sample_port], 1))

        result, count = port_manager.search(ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, port_id='port',
                                            switch_id='switch',
                                            room_number='room',
                                            terms='terms')

        assert [sample_port] == result
        assert 1 == count
        mock_port_repository.search_port_by.assert_called_once_with(ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET,
                                                                    port_id='port',
                                                                    switch_id='switch',
                                                                    room_number='room',
                                                                    terms='terms')

    def test_invalid_offset(self,
                            ctx,
                            port_manager: PortManager):
        with raises(IntMustBePositiveException):
            port_manager.search(ctx, offset=-1)

    def test_invalid_limit(self,
                           ctx,
                           port_manager: PortManager):
        with raises(IntMustBePositiveException):
            port_manager.search(ctx, limit=-1)


class TestCreate:

    @fixture
    def sample_mutation_req(self):
        return MutationRequest(port_number='port', room_number='room',
                               switch_id='switch',
                               rcom=42,
                               oid='oid',
                               )

    def test_happy_path(self,
                        ctx,
                        mock_port_repository: PortRepository,
                        sample_mutation_req: MutationRequest,
                        port_manager: PortManager):
        # Given...
        mock_port_repository.create_port = MagicMock()

        # When...
        port_manager.create(ctx, sample_mutation_req)

        # Expect...
        args = asdict(sample_mutation_req)
        mock_port_repository.create_port.assert_called_once_with(ctx, **args)

    def test_unknown_room(self,
                          ctx,
                          mock_port_repository: PortRepository,
                          sample_mutation_req: MutationRequest,
                          port_manager: PortManager):
        # Given...
        mock_port_repository.create_port = MagicMock(side_effect=InvalidRoomNumber)

        # When...
        with raises(RoomNotFound):
            port_manager.create(ctx, sample_mutation_req)

        # Expect..
        mock_port_repository.create_port.assert_called_once()

    def test_unknown_switch(self,
                            ctx,
                            mock_port_repository: PortRepository,
                            sample_mutation_req: MutationRequest,
                            port_manager: PortManager):
        # Given...
        mock_port_repository.create_port = MagicMock(side_effect=InvalidSwitchID)

        # When...
        with raises(SwitchNotFound):
            port_manager.create(ctx, sample_mutation_req)

        # Expect..
        mock_port_repository.create_port.assert_called_once()


class TestUpdate:

    @fixture
    def sample_mutation_req(self):
        return MutationRequest(
            port_number='port',
            room_number='room',
            switch_id='switch',
            rcom=42,
            oid='oid',
        )

    def test_happy_path(self,
                        ctx,
                        mock_port_repository: PortRepository,
                        sample_mutation_req: MutationRequest,
                        port_manager: PortManager):
        # Given...
        mock_port_repository.update_port = MagicMock()

        # When...
        port_manager.update(ctx, '1', sample_mutation_req)

        # Expect...
        args = asdict(sample_mutation_req)
        mock_port_repository.update_port.assert_called_once_with(ctx, port_id='1', **args)

    def test_unknown_room(self,
                          ctx,
                          mock_port_repository: PortRepository,
                          sample_mutation_req: MutationRequest,
                          port_manager: PortManager):
        # Given...
        mock_port_repository.update_port = MagicMock(side_effect=InvalidRoomNumber)

        # When...
        with raises(RoomNotFound):
            port_manager.update(ctx, '1', sample_mutation_req)

        # Expect..
        mock_port_repository.update_port.assert_called_once()

    def test_unknown_port(self,
                          ctx,
                          mock_port_repository: PortRepository,
                          sample_mutation_req: MutationRequest,
                          port_manager: PortManager):
        # Given...
        mock_port_repository.update_port = MagicMock(side_effect=PortNotFound)

        # When...
        with raises(PortNotFound):
            port_manager.update(ctx, '1', sample_mutation_req)

        # Expect..
        mock_port_repository.update_port.assert_called_once()

    def test_unknown_switch(self,
                            ctx,
                            mock_port_repository: PortRepository,
                            sample_mutation_req: MutationRequest,
                            port_manager: PortManager):
        # Given...
        mock_port_repository.update_port = MagicMock(side_effect=InvalidSwitchID)

        # When...
        with raises(SwitchNotFound):
            port_manager.update(ctx, '1', sample_mutation_req)

        # Expect..
        mock_port_repository.update_port.assert_called_once()


class TestDelete:
    def test_happy_path(self,
                        ctx,
                        mock_port_repository: PortRepository,
                        port_manager: PortManager):
        # Given...
        mock_port_repository.delete_port = MagicMock()

        # When...
        port_manager.delete(ctx, 'portID')

        # Expect...
        mock_port_repository.delete_port.assert_called_once_with(ctx, 'portID')

    def test_port_not_found(self,
                            ctx,
                            mock_port_repository: PortRepository,
                            port_manager: PortManager):
        # Given...
        mock_port_repository.delete_port = MagicMock(side_effect=PortNotFound)

        # When...
        with raises(PortNotFound):
            port_manager.delete(ctx, 'portID')


@fixture
def port_manager(
        mock_port_repository,
):
    return PortManager(
        port_repository=mock_port_repository
    )


@fixture
def mock_port_repository():
    return MagicMock(spec=PortRepository)
