# coding=utf-8
import json
from dataclasses import dataclass, asdict
from typing import List

from src.entity.room import Room
from src.exceptions import VlanNotFound, RoomNotFound
from src.use_case.interface.member_repository import NotFoundError
from src.use_case.interface.room_repository import RoomRepository
from src.use_case.util.exceptions import IntMustBePositiveException, MissingRequiredFieldError, RoomNumberMismatchError, \
    InvalidVLANNumberError
from src.use_case.util.mutation import Mutation, is_set
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class MutationRequest:
    room_number: str = Mutation.NOT_SET
    description: str = Mutation.NOT_SET
    phone_number: str = Mutation.NOT_SET
    vlan_number: str = Mutation.NOT_SET


class RoomManager:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def delete(self, ctx, room_number) -> None:
        """
        Delete a room from the database.

        User story: As an admin, I can delete a room, so I can remove rooms that do not exist.

        :raise RoomNotFound
        """
        try:
            self.room_repository.delete_room(ctx, room_number=room_number)
            LOG.info('room_delete', extra=log_extra(ctx, room_number=room_number))

        except NotFoundError as e:
            raise RoomNotFound() from e

    def get_by_number(self, ctx, room_number) -> Room:
        """
        Get a room from the database.

        User story: As an admin, I can get a room, so that see the room information.

        :raise RoomNotFound
        """
        result, _ = self.room_repository.search_room_by(ctx, room_number=room_number)
        LOG.info('room_get_by_number', extra=log_extra(ctx, room_number=room_number))
        if not result:
            raise RoomNotFound()

        return result[0]

    def search(self, ctx, limit=100, offset=0, terms=None) -> (List[Room], int):
        """
        Search a room in the database.

        User story: As an admin, I can search rooms, so that see the room information.

        :raise IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.room_repository.search_room_by(ctx, limit=limit, offset=offset, terms=terms)
        LOG.info('room_search', extra=log_extra(
            ctx,
            terms=terms,
        ))
        return result, count

    def update_or_create(self, ctx, room_number, mutation_request: MutationRequest) -> bool:
        """
        Create/Update a room from the database.

        User story: As an admin, I can modify a room, so that I change its description.
        :return: True if the room was created, false otherwise.

        :raise MissingRequiredFieldError
        :raise VlanNotFound
        :raise RoomNumberMismatchError
        """
        # Make sure all the fields set are valid.
        _validate_mutation_request(mutation_request)

        # Make sure all the necessary fields are set.
        if not is_set(mutation_request.room_number):
            raise MissingRequiredFieldError('room_number')

        room, _ = self.room_repository.search_room_by(ctx, room_number=room_number)
        if room:
            # [UPDATE] Room already exists, perform a whole update.

            # Create a dict with fields to update. If field is not provided in the mutation request, consider that it
            # should be None as it is a full update of the member.
            fields_to_update = asdict(mutation_request)
            fields_to_update = {k: v if is_set(v) else None for k, v in fields_to_update.items()}

            # This call will never throw a NotFoundError because we checked for the object existence before.
            try:
                self.room_repository.update_room(ctx, room_number, **fields_to_update)

            except InvalidVLANNumberError as e:
                raise VlanNotFound() from e

            # Log action.
            LOG.info('room_update', extra=log_extra(
                ctx,
                room_number=room_number,
                mutation=json.dumps(fields_to_update, sort_keys=True),
            ))

            return False
        else:
            # [CREATE] Room does not exist, create it.

            # Build a dict that will be transformed into a room. If a field is not set, consider that it should be
            #  None.
            if room_number != mutation_request.room_number:
                raise RoomNumberMismatchError()

            fields = asdict(mutation_request)
            fields = {k: v if is_set(v) else None for k, v in fields.items()}

            try:
                self.room_repository.create_room(ctx, **fields)

            except InvalidVLANNumberError as e:
                raise VlanNotFound() from e

            # Log action
            LOG.info('room_create', extra=log_extra(
                ctx,
                room_number=room_number,
                mutation=json.dumps(fields, sort_keys=True)
            ))

            return True


def _validate_mutation_request(req: MutationRequest):
    pass
