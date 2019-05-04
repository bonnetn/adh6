# coding=utf-8 import datetime import datetime import datetime
import datetime
from dataclasses import asdict
from pytest import fixture, raises, mark
from unittest import mock
from unittest.mock import MagicMock

from config import TEST_CONFIGURATION
from src.entity.member import Member
from src.exceptions import LogFetchError, NoPriceAssignedToThatDuration, MemberNotFoundError, UsernameMismatchError, \
    PasswordTooShortError, IntMustBePositive, MissingRequiredField, UnknownPaymentMethod, InvalidAdmin
from src.use_case.interface.logs_repository import LogsRepository
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.membership_repository import MembershipRepository
from src.use_case.interface.money_repository import MoneyRepository
from src.use_case.member_manager import MemberManager, FullMutationRequest, PartialMutationRequest
from src.util.hash import ntlm_hash
from test.unit.use_case.conftest import TEST_USERNAME, TEST_EMAIL, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_COMMENT, \
    TEST_ROOM_NUMBER, TEST_DATE1, TEST_DATE2, TEST_LOGS

INVALID_MUTATION_REQ_ARGS = [
    ('empty_email', {'email': ''}),
    ('empty_first_name', {'first_name': ''}),
    ('empty_last_name', {'last_name': ''}),
    ('empty_username', {'username': ''}),
    ('empty_room_number', {'room_number': ''}),

    ('invalid_email', {'email': 'not a valid email'}),
    ('invalid_username', {'username': 'this username is way too long'}),

    ('invalid_association_mode', {'association_mode': 'this is not a date'}),
    ('invalid_departure_date', {'departure_date': 'this is not a date'}),
]


class TestNewMembership:
    def test_happy_path(self, ctx,
                        mock_membership_repository: MagicMock,
                        mock_member_repository: MagicMock,
                        member_manager: MemberManager):
        # When...
        member_manager.new_membership(ctx, TEST_USERNAME, 1, 'cash', start_str=TEST_DATE1.isoformat())

        # Expect...
        expected_start_date = TEST_DATE1
        expected_end_date = TEST_DATE1 + datetime.timedelta(days=1)

        # Expect to create a new membership record...
        self._assert_membership_record_was_created(ctx, TEST_USERNAME, mock_membership_repository,
                                                   expected_start_date, expected_end_date)

        # And update the member object.
        mock_member_repository.update_member.assert_called_once_with(ctx, TEST_USERNAME,
                                                                     departure_date=expected_end_date.isoformat())

    def test_happy_path_without_start_time(self, ctx,
                                           mock_membership_repository: MagicMock,
                                           mock_member_repository: MagicMock,
                                           member_manager: MemberManager):
        # Given that now == TEST_DATE (monkey patch datetime.now())
        # See here: http://blog.xelnor.net/python-mocking-datetime/
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = TEST_DATE1

            # When...
            member_manager.new_membership(ctx, TEST_USERNAME, 1, 'card')

        # Expect...
        expected_start_date = TEST_DATE1
        expected_end_date = TEST_DATE1 + datetime.timedelta(days=1)

        # Expect to create a new membership record...
        self._assert_membership_record_was_created(ctx, TEST_USERNAME, mock_membership_repository,
                                                   expected_start_date, expected_end_date)

        # And update the member object.
        mock_member_repository.update_member.assert_called_once_with(ctx, TEST_USERNAME,
                                                                     departure_date=expected_end_date.isoformat())

    def test_invalid_duration(self, ctx,
                              mock_member_repository: MagicMock,
                              mock_membership_repository: MagicMock,
                              member_manager: MemberManager):
        # When...
        with raises(IntMustBePositive):
            member_manager.new_membership(ctx, TEST_USERNAME, -1, 'bank_cheque')

        # Expect that the database has not been touched.
        mock_member_repository.update_member.assert_not_called()
        mock_membership_repository.create_membership.assert_not_called()

    def test_no_price_for_duration(self, ctx,
                                   mock_member_repository: MagicMock,
                                   mock_membership_repository: MagicMock,
                                   member_manager: MemberManager):
        # When...
        with raises(NoPriceAssignedToThatDuration):
            member_manager.new_membership(ctx, TEST_USERNAME, 123456789, 'cash')

        # Expect that the database has not been touched.
        mock_member_repository.update_member.assert_not_called()
        mock_membership_repository.create_membership.assert_not_called()

    def test_member_not_found(self, ctx, mock_member_repository: MemberRepository, member_manager: MemberManager):
        # Given that the database cannot find the specified member.
        mock_member_repository.update_member = MagicMock(side_effect=MemberNotFoundError)

        with raises(MemberNotFoundError):
            member_manager.new_membership(ctx, TEST_USERNAME, 1, 'card')

    @mark.parametrize('exception', [UnknownPaymentMethod, InvalidAdmin])
    def test_fail_to_create_transaction(self, ctx,
                                        mock_membership_repository: MembershipRepository,
                                        mock_member_repository: MemberRepository,
                                        mock_money_repository: MoneyRepository,
                                        exception: Exception,
                                        member_manager: MemberManager):
        mock_member_repository.update_member = MagicMock()
        mock_money_repository.add_member_payment_record = MagicMock(side_effect=exception)

        # When...
        with raises(exception):
            member_manager.new_membership(ctx, TEST_USERNAME, 1, 'cash', start_str=TEST_DATE1.isoformat())

        # Expect...
        mock_member_repository.update_member.assert_not_called()

    @staticmethod
    def _assert_membership_record_was_created(ctx, user, repo, start_time, end_time):
        repo.create_membership.assert_called_once_with(
            ctx,
            user,
            start_time,
            end_time
        )


class TestGetByUsername:
    def test_happy_path(self, ctx,
                        mock_member_repository: MagicMock,
                        sample_member: Member,
                        member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # When...
        result = member_manager.get_by_username(ctx, TEST_USERNAME)

        # Expect...
        assert sample_member == result
        mock_member_repository.search_member_by.assert_called_once_with(ctx, username=TEST_USERNAME)

    def test_not_found(self, ctx,
                       mock_member_repository: MagicMock,
                       member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([], 0))

        # When...
        with raises(MemberNotFoundError):
            member_manager.get_by_username(ctx, TEST_USERNAME)

        # Expect...
        mock_member_repository.search_member_by.assert_called_once_with(ctx, username=TEST_USERNAME)


class TestSearch:
    def test_happy_path(self, ctx,
                        mock_member_repository: MagicMock,
                        sample_member: Member,
                        member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # When...
        test_terms = 'somthing to serach'
        test_offset = 42
        test_limit = 99
        result, count = member_manager.search(ctx, limit=test_limit, offset=test_offset,
                                              room_number=TEST_ROOM_NUMBER, terms=test_terms)

        # Expect...
        assert [sample_member] == result

        # Make sure that all the parameters are passed to the DB.
        mock_member_repository.search_member_by.assert_called_once_with(ctx,
                                                                        limit=test_limit,
                                                                        offset=test_offset,
                                                                        room_number=TEST_ROOM_NUMBER,
                                                                        terms=test_terms)

    def test_invalid_limit(self, ctx,
                           member_manager: MemberManager):
        # When...
        with raises(IntMustBePositive):
            member_manager.search(ctx, limit=-1)

    def test_invalid_offset(self, ctx,
                            member_manager: MemberManager):
        # When...
        with raises(IntMustBePositive):
            member_manager.search(ctx, limit=10, offset=-1)


class TestCreateOrUpdate:

    def test_create_happy_path(self, ctx,
                               mock_member_repository: MagicMock,
                               sample_mutation_request: FullMutationRequest,
                               member_manager: MemberManager):
        # Given that there is not user in the DB (user will be created).
        mock_member_repository.search_member_by = MagicMock(return_value=([], 0))

        # When...
        member_manager.update_or_create(ctx, TEST_USERNAME, sample_mutation_request)

        # Expect...
        mock_member_repository.create_member.assert_called_once_with(ctx, **asdict(sample_mutation_request))

    def test_update_happy_path(self, ctx,
                               mock_member_repository: MagicMock,
                               sample_mutation_request: FullMutationRequest,
                               sample_member: Member,
                               member_manager: MemberManager):
        # Given that there is a user in the DB (user will be updated).
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # Given a request that updates some fields.
        req = sample_mutation_request
        req.comment = "Updated comment."
        req.first_name = "George"
        req.last_name = "Dupuis"

        # When...
        member_manager.update_or_create(ctx, TEST_USERNAME, req)

        # Expect...
        mock_member_repository.update_member.assert_called_once_with(ctx, TEST_USERNAME, **asdict(req))
        mock_member_repository.create_member.assert_not_called()  # Do not create any member!

    @mark.parametrize('field', ['email', 'first_name', 'last_name', 'username', 'departure_date'])
    def test_update_without_required_field(self, ctx,
                                           mock_member_repository: MagicMock,
                                           sample_mutation_request: FullMutationRequest,
                                           sample_member: Member,
                                           field: str,
                                           member_manager: MemberManager):
        # Given that there is a user in the DB (user will be updated).
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # Given a request that updates some fields.
        req = sample_mutation_request
        req = FullMutationRequest(**{**asdict(req), **{field: None}})

        # When...
        with raises(MissingRequiredField):
            member_manager.update_or_create(ctx, TEST_USERNAME, req)

        # Expect...
        mock_member_repository.update_member.assert_not_called()
        mock_member_repository.create_member.assert_not_called()  # Do not create any member!

    def test_create_username_mismatch(self, ctx,
                                      mock_member_repository: MagicMock,
                                      sample_mutation_request: FullMutationRequest,
                                      member_manager: MemberManager):
        # Given a request that contains a different username than the one in the first argument.
        req = sample_mutation_request
        req.username = "abcdefgh"  # something different than the username provided in the 'username' argument

        # Given that there is not user in the DB (user will be created).
        mock_member_repository.search_member_by = MagicMock(return_value=([], 0))

        # When...
        with raises(UsernameMismatchError):
            member_manager.update_or_create(ctx, TEST_USERNAME, req)

        # Expect...
        mock_member_repository.create_member.assert_not_called()
        mock_member_repository.update_member.assert_not_called()


class TestUpdatePartially:
    def test_happy_path(self, ctx,
                        mock_member_repository: MagicMock,
                        member_manager: MemberManager):
        updated_comment = 'Updated comment.'
        req = PartialMutationRequest(comment=updated_comment)

        # When...
        member_manager.update_partially(ctx, TEST_USERNAME, req)

        # Expect...
        mock_member_repository.update_member.assert_called_once_with(ctx, TEST_USERNAME, comment=updated_comment)

    def test_not_found(self, ctx,
                       mock_member_repository: MagicMock,
                       member_manager: MemberManager):
        mock_member_repository.update_member = MagicMock(side_effect=MemberNotFoundError)

        # When...
        with raises(MemberNotFoundError):
            member_manager.update_partially(ctx, TEST_USERNAME, PartialMutationRequest(comment='Abc.'))

    @mark.parametrize('test_name, req_args', INVALID_MUTATION_REQ_ARGS)
    def test_invalid_mutation_req(self, ctx,
                                  member_manager: MemberManager,
                                  req_args: dict,
                                  test_name: str):
        req = PartialMutationRequest(**req_args)
        # When...
        with raises(ValueError):
            member_manager.update_partially(ctx, TEST_USERNAME, req)


class TestChangePassword:
    def test_happy_path(self, ctx,
                        mock_member_repository: MagicMock,
                        member_manager: MemberManager):
        # Given...
        new_password = 'updated password'
        new_password_hash = ntlm_hash(new_password)

        # When...
        member_manager.change_password(ctx, TEST_USERNAME, new_password)

        # Expect...
        mock_member_repository.update_member.assert_called_once_with(ctx, TEST_USERNAME, password=new_password_hash)

    def test_password_too_short(self, ctx,
                                mock_member_repository: MagicMock,
                                member_manager: MemberManager):
        # Given...
        new_password = '123'

        # When...
        with raises(PasswordTooShortError):
            member_manager.change_password(ctx, TEST_USERNAME, new_password)

        # Expect...
        mock_member_repository.update_member.assert_not_called()  # Do not update with weak password...

    def test_member_not_found(self, ctx,
                              mock_member_repository: MagicMock,
                              member_manager: MemberManager):
        # Given...
        new_password = 'updated password'
        mock_member_repository.update_member = MagicMock(side_effect=MemberNotFoundError)

        # When...
        with raises(MemberNotFoundError):
            member_manager.change_password(ctx, TEST_USERNAME, new_password)


class TestDelete:
    def test_happy_path(self, ctx,
                        mock_member_repository: MagicMock,
                        member_manager: MemberManager):
        # When...
        member_manager.delete(ctx, TEST_USERNAME)

        # Expect...
        mock_member_repository.delete_member.assert_called_once_with(ctx, TEST_USERNAME)

    def test_not_found(self, ctx,
                       mock_member_repository: MagicMock,
                       member_manager: MemberManager):
        # Given...
        mock_member_repository.delete_member = MagicMock(side_effect=MemberNotFoundError)

        # When...
        with raises(MemberNotFoundError):
            member_manager.delete(ctx, TEST_USERNAME)


class TestGetLogs:
    def test_happy_path(self, ctx,
                        mock_logs_repository: MagicMock,
                        mock_member_repository: MagicMock,
                        sample_member: Member,
                        member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))

        # When...
        result = member_manager.get_logs(ctx, TEST_USERNAME)

        # Expect...
        assert TEST_LOGS == result
        mock_logs_repository.get_logs.assert_called_once_with(ctx, TEST_USERNAME, [])

    def test_fetch_failed(self, ctx,
                          mock_logs_repository: MagicMock,
                          mock_member_repository: MagicMock,
                          sample_member: Member,
                          member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([sample_member], 1))
        mock_logs_repository.get_logs = MagicMock(side_effect=LogFetchError)

        # When...
        result = member_manager.get_logs(ctx, TEST_USERNAME)

        # Expect use case to 'fail open', do not throw any error, assume there is no log.
        assert [] == result

    def test_not_found(self, ctx,
                       mock_member_repository: MagicMock,
                       member_manager: MemberManager):
        # Given...
        mock_member_repository.search_member_by = MagicMock(return_value=([], 0))

        # When...
        with raises(MemberNotFoundError):
            member_manager.get_logs(ctx, TEST_USERNAME)


@fixture
def sample_mutation_request():
    return FullMutationRequest(
        email=TEST_EMAIL,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
        username=TEST_USERNAME,
        comment=TEST_COMMENT,
        association_mode=TEST_DATE2.isoformat(),
        departure_date=TEST_DATE1.isoformat(),
        room_number=TEST_ROOM_NUMBER,
    )


@fixture
def member_manager(
        mock_member_repository,
        mock_money_repository,
        mock_membership_repository,
        mock_logs_repository,
):
    return MemberManager(
        member_repository=mock_member_repository,
        money_repository=mock_money_repository,
        membership_repository=mock_membership_repository,
        logs_repository=mock_logs_repository,
        configuration=TEST_CONFIGURATION,
    )


@fixture
def mock_money_repository():
    return MagicMock(spec=MoneyRepository)


@fixture
def mock_member_repository():
    return MagicMock(spec=MemberRepository)


@fixture
def mock_membership_repository():
    return MagicMock(spec=MembershipRepository)


@fixture
def mock_logs_repository():
    r = MagicMock(spec=LogsRepository)
    r.get_logs = MagicMock(return_value=TEST_LOGS)
    return r
