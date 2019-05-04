# coding=utf-8
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.port import Port
from src.exceptions import RoomNotFound, SwitchNotFound, InvalidRoomNumber, InvalidSwitchID, \
    IntMustBePositiveException, MissingRequiredField
from src.use_case.interface.port_repository import PortRepository
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class MutationRequest:
    """
    Mutation request for a port. This represents the 'diff', that is going to be applied on the port object.
    """
    port_number: str
    switch_id: str
    rcom: int
    oid: Optional[str]
    room_number: Optional[str]

    def validate(self):
        """
        Validate the fields that are set in a MutationRequest.
        """
        if self.port_number is None:
            raise MissingRequiredField('port_number')

        if self.switch_id is None:
            raise MissingRequiredField('switch_id')

        if self.rcom is None:
            raise MissingRequiredField('rcom')


class PortManager:
    def __init__(self, port_repository: PortRepository):
        self.port_repository = port_repository

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, port_id=None, switch_id=None, room_number=None,
               terms=None) -> (
            List[Port], int):
        """
        Search ports in the database.
        User story: As an admin, I can search ports in the database, so I get all the ports from a room.

        :return: The list of the ports and the number of matches in the entire database.

        :raise IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.port_repository.search_port_by(ctx, limit=limit, offset=offset, port_id=port_id,
                                                            switch_id=switch_id, room_number=room_number, terms=terms)
        LOG.info("port_search",
                 extra=log_extra(ctx, port_id=port_id, switch_id=switch_id, room_number=room_number, terms=terms))

        return result, count

    def update(self, ctx, port_id, mutation_request: MutationRequest) -> None:
        """
        Update a port in the database.
        User story: As an admin, I can update a port in the database, so I can modify its description.

        :raise PortNotFound
        :raise SwitchNotFound
        :raise RoomNotFound
        """
        # Make sure the request is valid.
        mutation_request.validate()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}
        try:
            self.port_repository.update_port(ctx, port_id=port_id, **fields_to_update)
            LOG.info("port_update", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))

        except InvalidSwitchID as e:
            raise SwitchNotFound() from e

        except InvalidRoomNumber as e:
            raise RoomNotFound() from e

    def create(self, ctx, mutation_request: MutationRequest) -> str:
        """
        Create a port in the database.
        User story: As an admin, I can create a port in the database, so I can add a new port to a room.

        :return: the newly created port ID

        :raise ReadOnlyField
        :raise SwitchNotFound
        :raise RoomNotFound
        """
        # Make sure the request is valid.
        mutation_request.validate()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}
        try:
            port_id = self.port_repository.create_port(ctx, **fields_to_update)
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

        :raise PortNotFound
        """
        self.port_repository.delete_port(ctx, port_id)
