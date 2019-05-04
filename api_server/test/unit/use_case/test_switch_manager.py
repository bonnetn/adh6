from dataclasses import asdict
from pytest import fixture, raises, mark
from unittest.mock import MagicMock

from src.entity.switch import Switch
from src.exceptions import SwitchNotFoundError, MissingRequiredField, IntMustBePositive
from src.use_case.interface.switch_repository import SwitchRepository
from src.use_case.switch_manager import SwitchManager, MutationRequest

TEST_SWITCH_ID = '1'


class TestGetByID:
    def test_happy_path(self,
                        ctx,
                        mock_switch_repository: SwitchRepository,
                        sample_switch: Switch,
                        switch_manager: SwitchManager):
        mock_switch_repository.search_switches_by = MagicMock(return_value=([sample_switch], 1))
        result = switch_manager.get_by_id(ctx, TEST_SWITCH_ID)

        assert sample_switch == result
        mock_switch_repository.search_switches_by.assert_called_once()

    def test_switch_not_found(self,
                              ctx,
                              mock_switch_repository: SwitchRepository,
                              switch_manager: SwitchManager):
        mock_switch_repository.search_switches_by = MagicMock(return_value=([], 0))

        with raises(SwitchNotFoundError):
            switch_manager.get_by_id(ctx, TEST_SWITCH_ID)


class TestSearch:
    def test_happy_path(self,
                        ctx,
                        mock_switch_repository: SwitchRepository,
                        sample_switch: Switch,
                        switch_manager: SwitchManager):
        mock_switch_repository.search_switches_by = MagicMock(return_value=([sample_switch], 1))
        result, count = switch_manager.search(ctx, limit=42, offset=2, terms='abc')

        assert [sample_switch] == result
        assert 1 == count
        mock_switch_repository.search_switches_by.assert_called_once_with(ctx, limit=42, offset=2, terms='abc')

    def test_offset_negative(self,
                             ctx,
                             switch_manager: SwitchManager):
        with raises(IntMustBePositive):
            switch_manager.search(ctx, offset=-1)

    def test_limit_negative(self,
                            ctx,
                            switch_manager: SwitchManager):
        with raises(IntMustBePositive):
            switch_manager.search(ctx, limit=-1)


class TestUpdate:
    def test_happy_path(self,
                        ctx,
                        mock_switch_repository: SwitchRepository,
                        switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock()

        switch_manager.update(ctx, '2', req)

        mock_switch_repository.update_switch.assert_called_once_with(ctx, switch_id='2', **asdict(req))

    def test_switch_not_found(self,
                              ctx,
                              mock_switch_repository: SwitchRepository,
                              switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock(side_effect=SwitchNotFoundError)

        with raises(SwitchNotFoundError):
            switch_manager.update(ctx, '2', req)

    def test_missing_required_field(self,
                                    ctx,
                                    mock_switch_repository: SwitchRepository,
                                    switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        req.community = None
        mock_switch_repository.update_switch = MagicMock()

        with raises(MissingRequiredField):
            switch_manager.update(ctx, '2', req)

        mock_switch_repository.update_switch.assert_not_called()

    @mark.parametrize('field,value', [
        ('ip_v4', None),
        ('ip_v4', 'not an ipv4 address'),
        ('description', None),
        ('community', None),
    ])
    def test_invalid_mutation_request(self,
                                      ctx,
                                      mock_switch_repository: SwitchRepository,
                                      field: str,
                                      value,
                                      switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        req = MutationRequest(**{**asdict(req), **{field: value}})
        mock_switch_repository.update_switch = MagicMock()

        with raises(ValueError):
            switch_manager.update(ctx, '2', req)


class TestCreate:
    def test_happy_path(self,
                        ctx, mock_switch_repository: SwitchRepository, switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='157.159.123.123',
            community='ip',
        )
        mock_switch_repository.create_switch = MagicMock()

        switch_manager.create(ctx, req)

        mock_switch_repository.create_switch.assert_called_once_with(ctx, description=req.description, ip_v4=req.ip_v4,
                                                                     community=req.community)


class TestDelete:
    def test_happy_path(self,
                        ctx,
                        mock_switch_repository: SwitchRepository,
                        switch_manager: SwitchManager):
        mock_switch_repository.delete_switch = MagicMock()

        switch_manager.delete(ctx, TEST_SWITCH_ID)

        mock_switch_repository.delete_switch.assert_called_once_with(ctx, TEST_SWITCH_ID)

    def test_not_found(self,
                       ctx,
                       mock_switch_repository: SwitchRepository,
                       switch_manager: SwitchManager):
        mock_switch_repository.delete_switch = MagicMock(side_effect=SwitchNotFoundError)

        with raises(SwitchNotFoundError):
            switch_manager.delete(ctx, TEST_SWITCH_ID)


@fixture
def switch_manager(mock_switch_repository, ):
    return SwitchManager(
        switch_repository=mock_switch_repository
    )


@fixture
def mock_switch_repository():
    return MagicMock(spec=SwitchRepository)
