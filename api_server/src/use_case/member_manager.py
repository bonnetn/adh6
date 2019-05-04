# coding=utf-8
""" Use cases (business rule layer) of everything related to members. """
import datetime
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from src.constants import DEFAULT_OFFSET, DEFAULT_LIMIT
from src.entity.member import Member
from src.exceptions import InvalidAdmin, UnknownPaymentMethod, LogFetchError, NoPriceAssignedToThatDurationException, \
    MemberNotFound, UsernameMismatchError, PasswordTooShortError, InvalidEmail, \
    IntMustBePositiveException, StringMustNotBeEmptyException, InvalidDate, MissingRequiredField
from src.use_case.interface.logs_repository import LogsRepository
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.membership_repository import MembershipRepository
from src.use_case.interface.money_repository import MoneyRepository
from src.util.validator import is_email, is_empty, is_date
from src.util.context import log_extra
from src.util.date import string_to_date
from src.util.hash import ntlm_hash
from src.util.log import LOG


@dataclass
class PartialMutationRequest:
    """
    Mutation request for a member. This represents the 'diff', that is going to be applied on the member object.

    If a field is set to None, field be left untouched.
    """
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    comment: Optional[str] = None
    departure_date: Optional[str] = None
    association_mode: Optional[str] = None
    room_number: Optional[str] = None

    def validate(self):
        # EMAIL:
        if self.email and not is_email(self.email):
            raise InvalidEmail(self.email)

        # FIRST_NAME:
        if self.first_name is not None and is_empty(self.first_name):
            raise StringMustNotBeEmptyException('first_name')

        # LAST_NAME:
        if self.last_name is not None and is_empty(self.last_name):
            raise StringMustNotBeEmptyException('last_name')

        # USERNAME:
        if self.username is not None:
            if is_empty(self.username):
                raise StringMustNotBeEmptyException('username')

            if len(self.username) > 9 or len(self.username) < 7:
                raise ValueError('username must be between 7 and 9 characters long')

        # COMMENT:
        # Nothing to validate...

        # DEPARTURE_DATE:
        if self.departure_date is not None and not is_date(self.departure_date):
            raise InvalidDate(self.departure_date)

        # ASSOCIATION_MODE:
        if self.association_mode is not None and not is_date(self.association_mode):
            raise InvalidDate(self.departure_date)

        # ROOM_NUMBER:
        if self.room_number is not None and is_empty(self.room_number):
            raise StringMustNotBeEmptyException('room_number')


@dataclass
class FullMutationRequest(PartialMutationRequest):
    """
    Mutation request for a member. This represents the 'diff', that is going to be applied on the member object.

    If a field is set to None, field will be cleared in the database.
    """
    email: str
    first_name: str
    last_name: str
    username: str
    departure_date: str
    comment: Optional[str]
    association_mode: Optional[str]
    room_number: Optional[str]

    def validate(self):
        # EMAIL:
        if self.email is None:
            raise MissingRequiredField('email')

        # FIRST_NAME:
        if self.first_name is None:
            raise MissingRequiredField('first_name')

        # LAST_NAME:
        if self.last_name is None:
            raise MissingRequiredField('last_name')

        # USERNAME:
        if self.username is None:
            raise MissingRequiredField('username')

        # DEPARTURE_DATE:
        if self.departure_date is None:
            raise MissingRequiredField('departure_date')

        super().validate()


class MemberManager:
    """
    Implements all the use cases related to member management.
    """

    def __init__(self,
                 member_repository: MemberRepository,
                 membership_repository: MembershipRepository,
                 logs_repository: LogsRepository,
                 money_repository: MoneyRepository,
                 configuration):
        self.member_repository = member_repository
        self.membership_repository = membership_repository
        self.logs_repository = logs_repository
        self.money_repository = money_repository
        self.config = configuration

    def new_membership(self, ctx, username, duration, payment_method, start_str=None) -> None:
        """
        Core use case of ADH. Registers a membership.

        User story: As an admin, I can create a new membership record, so that a member can have internet access.
        :param ctx: context
        :param username: username
        :param duration: duration of the membership in days
        :param start_str: optional start date of the membership

        :raise IntMustBePositiveException
        :raise NoPriceAssignedToThatDurationException
        :raise MemberNotFound
        :raise InvalidAdmin
        :raise UnknownPaymentMethod
        """
        if start_str is None:
            return self.new_membership(ctx, username, duration, payment_method,
                                       start_str=datetime.datetime.now().isoformat())

        if duration < 0:
            raise IntMustBePositiveException('duration')

        if duration not in self.config.PRICES:
            LOG.warn("create_membership_record_no_price_defined", extra=log_extra(ctx, duration=duration))
            raise NoPriceAssignedToThatDurationException()

        start = string_to_date(start_str)
        end = start + datetime.timedelta(days=duration)

        # TODO check price.
        try:
            price = self.config.PRICES[duration]  # Expresed in EUR.
            price_in_cents = price * 100  # Expressed in cents of EUR.
            duration_str = self.config.DURATION_STRING.get(duration, '')
            title = f'Internet - {duration_str}'

            self.money_repository.add_member_payment_record(ctx, price_in_cents, title, username, payment_method)
            self.membership_repository.create_membership(ctx, username, start, end)
            self.member_repository.update_member(ctx, username, departure_date=end.isoformat())

        except InvalidAdmin:
            LOG.warn("create_membership_record_admin_not_found", extra=log_extra(ctx))
            raise

        except UnknownPaymentMethod:
            LOG.warn("create_membership_record_unknown_payment_method",
                     extra=log_extra(ctx, payment_method=payment_method))
            raise

        LOG.info("create_membership_record", extra=log_extra(
            ctx,
            username=username,
            duration_in_days=duration,
            start_date=start.isoformat()
        ))

    def get_by_username(self, ctx, username) -> Member:
        """
        User story: As an admin, I can see the profile of a member, so that I can help her/him.

        :raise MemberNotFound
        """
        result, _ = self.member_repository.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFound()

        # Log action.
        LOG.info('member_get_by_username', extra=log_extra(
            ctx,
            username='username'
        ))
        return result[0]

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, room_number=None, terms=None) -> (
            List[Member], int):
        """
        search member in the database.

        user story: as an admin, i want to have a list of members with some filters, so that i can browse and find
        members.

        :raise intmustbepositiveexception
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.member_repository.search_member_by(ctx,
                                                                limit=limit,
                                                                offset=offset,
                                                                room_number=room_number,
                                                                terms=terms)

        # Log action.
        LOG.info('member_search', extra=log_extra(
            ctx,
            room_number=room_number,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, username, mutation_request: FullMutationRequest) -> bool:
        """
        Create/Update member from the database.

        User story: As an admin, I can register a new profile, so that I can add a membership with their profile.
        :return: True if the member was created, false otherwise.

        :raise InvalidEmailError
        :raise InvalidRoomNumberError
        :raise MissingRequiredFieldError
        :raise StringMustNotBeEmptyException
        :raise UsernameMismatchError
        """
        # Make sure all the fields set are valid.
        mutation_request.validate()

        # Make sure all the necessary fields are set.
        member, _ = self.member_repository.search_member_by(ctx, username=username)
        if member:
            # [UPDATE] Member already exists, perform a whole update.

            # Create a dict with fields to update. If field is not provided in the mutation request, consider that it
            # should be None as it is a full update of the member.
            fields_to_update = asdict(mutation_request)
            fields_to_update = {k: v for k, v in fields_to_update.items()}

            # This call will never throw a MemberNotFound because we checked for the object existence before.
            self.member_repository.update_member(ctx, username, **fields_to_update)

            # Log action.
            LOG.info('member_whole_update', extra=log_extra(
                ctx,
                username=username,
                mutation=json.dumps(fields_to_update, sort_keys=True, default=str),
            ))

            return False
        else:
            # [CREATE] Member does not exist, create it.

            # Build a dict that will be transformed into a member. If a field is not set, consider that it should be
            # None.
            if username != mutation_request.username:
                raise UsernameMismatchError()

            mutation_request.username = username  # Just in case it has not been specified in the body.
            fields = asdict(mutation_request)
            fields = {k: v for k, v in fields.items()}

            self.member_repository.create_member(ctx, **fields)

            # Log action
            LOG.info('member_create', extra=log_extra(
                ctx,
                username=username,
                mutation=json.dumps(fields, sort_keys=True, default=str)
            ))

            return True

    def update_partially(self, ctx, username, mutation_request: PartialMutationRequest) -> None:
        """
        User story: As an admin, I can modify some of the fields of a profile, so that I can update the information of
        a member.

        :raise MemberNotFound
        """
        # Perform all the checks on the validity of the data in the mutation request.
        mutation_request.validate()

        # Create a dict with all the changed field. If a field is None it will not be put in the dict, and the
        # field will not be updated.
        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}

        self.member_repository.update_member(ctx, username, **fields_to_update)

        # Log action.
        LOG.info('member_partial_update', extra=log_extra(
            ctx,
            username=username,
            mutation=json.dumps(fields_to_update, sort_keys=True, default=str)
        ))

    def change_password(self, ctx, username, password) -> None:
        """
        User story: As an admin, I can set the password of a user, so that they can connect using their credentials.
        Change the password of a member.

        BE CAREFUL: do not log the password or store it unhashed.

        :raise PasswordTooShortError
        :raise MemberNotFound
        """

        if len(password) <= 6:  # It's a bit low but eh...
            raise PasswordTooShortError()

        # Overwrite password variable by its hash, now that the checks are done, we don't need the cleartext anymore.
        # Still, be careful not to log this field!
        password = ntlm_hash(password)

        self.member_repository.update_member(ctx, username, password=password)

        LOG.info('member_password_update', extra=log_extra(
            ctx,
            username=username,
        ))

    def delete(self, ctx, username) -> None:
        """
        User story: As an admin, I can remove a profile, so that their information is not in our system.

        :raise MemberNotFound
        """

        self.member_repository.delete_member(ctx, username)

        # Log action.
        LOG.info('member_delete', extra=log_extra(
            ctx,
            username=username,
        ))

    def get_logs(self, ctx, username) -> List[str]:
        """
        User story: As an admin, I can retrieve the logs of a member, so I can help him troubleshoot their connection
        issues.

        :raise MemberNotFound
        """
        # Fetch all the devices of the member to put them in the request
        # all_devices = get_all_devices(s)
        # q = s.query(all_devices, Adherent.login.label("login"))
        # q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)
        # q = q.filter(Adherent.login == username)
        # mac_tbl = list(map(lambda x: x.mac, q.all()))

        # Check that the user exists in the system.
        result, _ = self.member_repository.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFound()

        # Do the actual log fetching.
        try:
            # TODO: Fetch all the devices and put them into this request.
            logs = self.logs_repository.get_logs(ctx, username, [])

            LOG.info('member_get_logs', extra=log_extra(
                ctx,
                username=username,
            ))

            return logs

        except LogFetchError:
            LOG.warning("log_fetch_failed", extra=log_extra(ctx, username=username))
            return []  # We fail open here.
