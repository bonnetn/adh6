# coding=utf-8
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.room import Room
from src.exceptions import VLANNotFound, RoomNotFound, RoomNumberMismatchError, MissingRequiredField, \
    InvalidVLANNumber, IntMustBePositiveException
from src.use_case.interface.room_repository import RoomRepository
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class MutationRequest:
    room_number: str
    description: str
    phone_number: Optional[str]
    vlan_number: str

    def validate(self):
        if self.room_number is None:
            raise MissingRequiredField('room_number')

        if self.description is None:
            raise MissingRequiredField('description')

        if self.vlan_number is None:
            raise MissingRequiredField('vlan_number')


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

        except RoomNotFound as e:
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

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None) -> (List[Room], int):
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
        mutation_request.validate()

        room, _ = self.room_repository.search_room_by(ctx, room_number=room_number)
        if room:
            # [UPDATE] Room already exists, perform a whole update.

            # Create a dict with fields to update. If field is not provided in the mutation request, consider that it
            # should be None as it is a full update of the member.
            fields_to_update = asdict(mutation_request)
            fields_to_update = {k: v for k, v in fields_to_update.items()}

            # This call will never throw a RoomNotFound because we checked for the object existence before.
            try:
                self.room_repository.update_room(ctx, room_number, **fields_to_update)

            except InvalidVLANNumber as e:
                raise VLANNotFound() from e

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
            fields = {k: v for k, v in fields.items()}

            try:
                self.room_repository.create_room(ctx, **fields)

            except InvalidVLANNumber as e:
                raise VLANNotFound() from e

            # Log action
            LOG.info('room_create', extra=log_extra(
                ctx,
                room_number=room_number,
                mutation=json.dumps(fields, sort_keys=True)
            ))

            return True
