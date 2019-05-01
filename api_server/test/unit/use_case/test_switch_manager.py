from dataclasses import asdict
from pytest import fixture, raises
from unittest.mock import MagicMock

from src.entity.switch import Switch
from src.exceptions import SwitchNotFound
from src.use_case.interface.member_repository import NotFoundError
from src.use_case.interface.switch_repository import SwitchRepository
from src.use_case.port_manager import ReadOnlyField
from src.use_case.switch_manager import SwitchManager, MutationRequest
from src.use_case.util.exceptions import IntMustBePositiveException, MissingRequiredFieldError

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

        with raises(SwitchNotFound):
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
        with raises(IntMustBePositiveException):
            switch_manager.search(ctx, offset=-1)

    def test_limit_negative(self,
                            ctx,
                            switch_manager: SwitchManager):
        with raises(IntMustBePositiveException):
            switch_manager.search(ctx, limit=-1)


class TestUpdate:
    def test_happy_path(self,
                        ctx,
                        mock_switch_repository: SwitchRepository,
                        switch_manager: SwitchManager):
        req = MutationRequest(
            switch_id='2',
            description='desc',
            ip_v4='ip',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock()

        switch_manager.update(ctx, req)

        mock_switch_repository.update_switch.assert_called_once_with(ctx, **asdict(req))

    def test_switch_not_found(self,
                              ctx,
                              mock_switch_repository: SwitchRepository,
                              switch_manager: SwitchManager):
        req = MutationRequest(
            switch_id='2',
            description='desc',
            ip_v4='ip',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock(side_effect=NotFoundError)

        with raises(SwitchNotFound):
            switch_manager.update(ctx, req)

    def test_missing_required_field(self,
                                    ctx,
                                    mock_switch_repository: SwitchRepository,
                                    switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='ip',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock()

        with raises(MissingRequiredFieldError):
            switch_manager.update(ctx, req)

        mock_switch_repository.update_switch.assert_not_called()


class TestCreate:
    def test_happy_path(self,
                        ctx, mock_switch_repository: SwitchRepository, switch_manager: SwitchManager):
        req = MutationRequest(
            description='desc',
            ip_v4='ip',
            community='ip',
        )
        mock_switch_repository.create_switch = MagicMock()

        switch_manager.create(ctx, req)

        mock_switch_repository.create_switch.assert_called_once_with(ctx, description=req.description, ip_v4=req.ip_v4,
                                                                     community=req.community)

    def test_cannot_set_id(self,
                           ctx,
                           mock_switch_repository: SwitchRepository,
                           switch_manager: SwitchManager):
        req = MutationRequest(
            switch_id='should not be able to set a ID at creation',
            description='desc',
            ip_v4='ip',
            community='ip',
        )
        mock_switch_repository.update_switch = MagicMock()

        with raises(ReadOnlyField):
            switch_manager.create(ctx, req)

        mock_switch_repository.update_switch.assert_not_called()


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
        mock_switch_repository.delete_switch = MagicMock(side_effect=NotFoundError)

        with raises(SwitchNotFound):
            switch_manager.delete(ctx, TEST_SWITCH_ID)


@fixture
def switch_manager(mock_switch_repository, ):
    return SwitchManager(
        switch_repository=mock_switch_repository
    )


@fixture
def mock_switch_repository():
    return MagicMock(spec=SwitchRepository)
