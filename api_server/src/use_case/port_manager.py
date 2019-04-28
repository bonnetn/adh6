# coding=utf-8
import json
from dataclasses import dataclass, asdict
from typing import List

from src.entity.port import Port
from src.exceptions import RoomNotFound, SwitchNotFound, PortNotFound
from src.use_case.exceptions import IntMustBePositiveException, MissingRequiredFieldError
from src.use_case.interface.member_repository import NotFoundError
from src.use_case.interface.port_repository import PortRepository, InvalidRoomNumber, InvalidSwitchID
from src.use_case.mutation import Mutation, _is_set
from src.util.context import log_extra
from src.util.log import LOG


class ReadOnlyField(ValueError):
    pass


@dataclass
class MutationRequest:
    """
    Mutation request for a port. This represents the 'diff', that is going to be applied on the port object.
    """
    id: str = Mutation.NOT_SET
    port_number: str = Mutation.NOT_SET
    room_number: str = Mutation.NOT_SET
    switch_id: str = Mutation.NOT_SET
    rcom: int = Mutation.NOT_SET
    oid: str = Mutation.NOT_SET


class PortManager:
    def __init__(self, port_storage: PortRepository):
        self.port_storage = port_storage

    def search(self, ctx, limit=100, offset=0, port_id=None, switch_id=None, room_number=None, terms=None) -> (
            List[Port], int):
        """
        Search ports in the database.
        User story: As an admin, I can search ports in the database, so I get all the ports from a room.

        :return: The list of the ports and the number of matches in the entire database.

        :raises IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.port_storage.search_port_by(ctx, limit=limit, offset=offset, port_id=port_id,
                                                         switch_id=switch_id, room_number=room_number, terms=terms)
        LOG.info("port_search",
                 extra=log_extra(ctx, port_id=port_id, switch_id=switch_id, room_number=room_number, terms=terms))

        return result, count

    def update(self, ctx, mutation_request: MutationRequest) -> None:
        """
        Update a port in the database.
        User story: As an admin, I can update a port in the database, so I can modify its description.

        :raises PortNotFound
        :raises SwitchNotFound
        :raises RoomNotFound
        """
        # Make sure the request is valid.
        _validate_mutation_request(mutation_request)

        if not _is_set(mutation_request.id):
            raise MissingRequiredFieldError('id')

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if _is_set(v)}
        try:
            self.port_storage.update_port(ctx, **fields_to_update)
            LOG.info("port_update", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))

        except InvalidSwitchID as e:
            raise SwitchNotFound() from e

        except InvalidRoomNumber as e:
            raise RoomNotFound() from e

        except NotFoundError as e:
            raise PortNotFound() from e

    def create(self, ctx, mutation_request: MutationRequest) -> str:
        """
        Create a port in the database.
        User story: As an admin, I can create a port in the database, so I can add a new port to a room.

        :return: the newly created port ID

        :raises ReadOnlyField
        :raises SwitchNotFound
        :raises RoomNotFound
        """
        # Make sure the request is valid.
        _validate_mutation_request(mutation_request)

        if _is_set(mutation_request.id):
            raise ReadOnlyField()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if _is_set(v)}
        try:
            port_id = self.port_storage.create_port(ctx, **fields_to_update)
            LOG.info("port_create", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))
            return port_id

        except InvalidSwitchID as e:
            raise SwitchNotFound() from e

        except InvalidRoomNumber as e:
            raise RoomNotFound() from e

    def delete(self, ctx, port_id: str):
        """
        Delete a port from the database.
        User story: As an admin, I can delete a port, so I can remove old ports from the DB.

        :raises PortNotFound
        """
        try:
            self.port_storage.delete_port(ctx, port_id)

        except NotFoundError as e:
            raise PortNotFound() from e


def _validate_mutation_request(req: MutationRequest):
    """
    Validate the fields that are set in a MutationRequest.
    """
    pass
