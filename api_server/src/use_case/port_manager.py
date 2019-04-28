# coding=utf-8
import json
from dataclasses import dataclass, asdict
from typing import List

from src.entity.port import Port
from src.exceptions import RoomNotFound, SwitchNotFound
from src.use_case.exceptions import IntMustBePositiveException
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

    def search(self, ctx, limit=100, offset=0, switch_id=None, room_number=None, terms=None) -> (List[Port], int):
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.port_storage.search_port_by(ctx, limit=limit, offset=offset, switch_id=switch_id,
                                                         room_number=room_number, terms=terms)
        LOG.info("port_search", extra=log_extra(ctx, switch_id=switch_id, room_number=room_number, terms=terms))

        return result, count

    def create(self, ctx, mutation_request: MutationRequest) -> str:
        """ [API] Create a port in the database """
        # Make sure the request is valid.
        _validate_mutation_request(mutation_request)

        # Make sure the user is not trying to control the ID (it will be automatically populated).
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


def _validate_mutation_request(req: MutationRequest):
    """
    Validate the fields that are set in a MutationRequest.
    """
    pass
