import datetime
import json
import logging
from enum import Enum

from attr import dataclass, asdict

from CONFIGURATION import PRICES
from adh.constants import CTX_ADMIN
from adh.exceptions import IntMustBePositiveException, MemberNotFound, StringMustNotBeEmptyException
from adh.use_case.interface.logs_repository import LogsRepository, LogFetchError
from adh.use_case.interface.member_repository import MemberRepository, NotFoundError
from adh.use_case.interface.membership_repository import MembershipRepository
from adh.util.checks import is_email
from adh.util.date import string_to_date
from adh.util.hash import ntlm_hash


class Mutation(Enum):
    NOT_SET = 1


@dataclass
class MutationRequest:
    email: str = Mutation.NOT_SET
    first_name: str = Mutation.NOT_SET
    last_name: str = Mutation.NOT_SET
    username: str = Mutation.NOT_SET
    departure_date: str = Mutation.NOT_SET
    comment: str = Mutation.NOT_SET
    association_mode: str = Mutation.NOT_SET
    room_number: int = Mutation.NOT_SET


class MemberManager:
    def __init__(self,
                 member_storage: MemberRepository,
                 membership_storage: MembershipRepository,
                 logs_storage: LogsRepository):
        self.member_storage = member_storage
        self.membership_storage = membership_storage
        self.logs_storage = logs_storage

    def new_membership(self, ctx, username, duration, start_str=None):
        """
        Core use case of ADH. Registers a membership.

        User story: As an admin, I can create a new membership record, so that a member can have internet access.
        :param duration: duration of the membership in days
        :param start_str: optional start date of the membership
        """
        if username is None:
            raise ValueError('username is required')

        if duration is None:
            raise ValueError('duration is required')

        if start_str is None:
            raise ValueError('start date is required')

        if duration < 0:
            raise IntMustBePositiveException('duration')

        if duration not in PRICES:
            raise ValueError('there is no price assigned to that duration')

        if start_str is None:
            start = datetime.datetime.now().date()
        else:
            start = string_to_date(start_str)

        end = start + datetime.timedelta(days=duration)

        try:
            self.membership_storage.add_membership(ctx, username, start, end)
            self.member_storage.update_member(ctx, username, departure_date=end)
        except NotFoundError:
            raise MemberNotFound()

        admin = ctx.get(CTX_ADMIN)
        logging.info("%s created a membership record for %s of %s days starting from %s",
                     admin.login, username, duration, start.isoformat())

    def get_by_username(self, ctx, username):
        """
        User story: As an admin, I can see the profile of a member, so that I can help her/him.
        """
        if not username:
            raise ValueError('username not provided')

        result, _ = self.member_storage.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFound()

        # Log action.
        admin = ctx.get(CTX_ADMIN)
        logging.info("%s fetched the member %s", admin.login, username)
        return result[0]

    def search(self, ctx, limit, offset=0, room_number=None, terms=None):
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.member_storage.search_member_by(ctx,
                                                             limit=limit,
                                                             offset=offset,
                                                             room_number=room_number,
                                                             terms=terms)

        # Log action.
        logging.info("%s fetched the member list", ctx.get(CTX_ADMIN))
        return result, count

    def create_or_update(self, ctx, username, mutation_request: MutationRequest) -> bool:
        """
        Create/Update member from the database.
        User story: As an admin, I can register a new profile, so that I can add a membership with their profile.
        :return: True if the member was created, false otherwise.
        """
        admin = ctx.get(CTX_ADMIN)

        # Make sure all the fields set are valid.
        _validate_mutation_request(mutation_request)

        member, _ = self.member_storage.search_member_by(ctx, username=username)
        if member:
            # [UPDATE] Member already exists, perform a whole update.

            # Make sure all the necessary fields are set.
            if not _is_set(mutation_request.username):
                raise ValueError('username is a required field')

            # Create a dict with fields to update. If field is not provided in the mutation request, consider that it
            # should be None as it is a full update of the member.
            fields_to_update = asdict(mutation_request)
            fields_to_update = {k: v if _is_set(v) else None for k, v in fields_to_update.items()}

            self.member_storage.update_member(ctx, username, **fields_to_update)

            # Log action.
            logging.info("%s updated the member %s\n%s",
                         admin.login, username, json.dumps(fields_to_update, sort_keys=True, default=str))

            return False
        else:
            # [CREATE] Member does not exist, create it.

            # Build a dict that will be transformed into a member. If a field is not set, consider that it should be
            # None.
            if _is_set(mutation_request.username) and username != mutation_request.username:
                raise ValueError('cannot create member with 2 different usernames')

            mutation_request.username = username  # Just in case it has not been specified in the body.
            fields = asdict(mutation_request)
            fields = {k: v if _is_set(v) else None for k, v in fields.items()}
            object

            self.member_storage.create_member(ctx, **fields)

            # Log action
            logging.info("%s created the member %s\n%s",
                         admin.login, username, json.dumps(fields, sort_keys=True, default=str))

            return True

    def update_partially(self, ctx, username, mutation_request: MutationRequest):
        """
        User story: As an admin, I can modify some of the fields of a profile, so that I can update the information of
        a member.
        """
        # Perform all the checks on the validity of the data in the mutation request.
        _validate_mutation_request(mutation_request)

        # Create a dict with all the changed field. If a field in 'NOT_SET' it will not be put in the dict, and the
        # field will not be updated.
        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if _is_set(v)}

        self.member_storage.update_member(ctx, username, **fields_to_update)

        # Log action.
        admin = ctx.get(CTX_ADMIN)
        logging.info("%s updated the member %s\n%s",
                     admin.login, username, json.dumps(fields_to_update, sort_keys=True, default=str))

    def change_password(self, ctx, username, password):
        """
        User story: As an admin, I can set the password of a user, so that they can connect using their credentials.
        Change the password of a member.
        BE CAREFUL: do not log the password or store it unhashed.
        """
        if username is None:
            raise ValueError('username is required')

        if password is None:
            raise ValueError('password is required')

        if len(password) <= 6:  # It's a bit low but eh...
            raise ValueError('password should be longer')

        # Overwrite password variable by its hash, now that the checks are done, we don't need the cleartext anymore.
        # Still, be careful not to log this field!
        password = ntlm_hash(password)

        try:
            self.member_storage.update_member(ctx, username, password=password)
        except NotFoundError:
            raise MemberNotFound()

        admin = ctx.get(CTX_ADMIN)
        logging.info("%s updated the password of %s", admin.login, username)

    def delete(self, ctx, username):
        """
        User story: As an admin, I can remove a profile, so that their information is not in our system.
        """
        if not username:
            raise ValueError('username not provided')

        try:
            self.member_storage.delete_member(ctx, username)

            # Log action.
            admin = ctx.get(CTX_ADMIN)
            logging.info("%s deleted the member %s", admin.login, username)
        except ValueError:
            raise MemberNotFound()

    def get_logs(self, ctx, username):
        """
        User story: As an admin, I can retrieve the logs of a member, so I can help him troubleshoot their connection
        issues.
        """
        if not username:
            raise ValueError('username not provided')

        # Check that the user exists in the system.
        result, _ = self.member_storage.search_member_by(ctx, username=username)
        if not result:
            raise MemberNotFound()

        # Do the actual log fetching.
        try:
            logs = self.logs_storage.get_logs(ctx, username, [])

            admin = ctx.get(CTX_ADMIN)
            logging.info("%s fetched the logs of %s", admin.login, username)

            return logs

        except LogFetchError:
            logging.warn("Log fetching failed, returning empty response.")
            return []  # We fail open here.

        # Fetch all the devices of the member to put them in the request
        # all_devices = get_all_devices(s)
        # q = s.query(all_devices, Adherent.login.label("login"))
        # q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)
        # q = q.filter(Adherent.login == username)
        # mac_tbl = list(map(lambda x: x.mac, q.all()))


def _is_set(v):
    """
    Check if a field in a MutationRequest is set.
    """
    return v != Mutation.NOT_SET


def _validate_mutation_request(req: MutationRequest):
    """
    Validate the fields that are set in a MutationRequest.
    """
    if _is_set(req.email) and not is_email(req.email):
        raise ValueError('invalid email')

    if req.first_name == '':
        raise StringMustNotBeEmptyException('first_name')

    if req.last_name == '':
        raise StringMustNotBeEmptyException('last_name')

    if req.username == '':
        raise StringMustNotBeEmptyException('username')

    if req.comment == '':
        raise StringMustNotBeEmptyException('comment')

    if _is_set(req.room_number) and req.room_number < 0:
        raise StringMustNotBeEmptyException('room number')
