import json
from dataclasses import dataclass, asdict
from typing import List

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.switch import Switch
from src.exceptions import SwitchNotFound
from src.use_case.interface.member_repository import NotFoundError
from src.use_case.interface.switch_repository import SwitchRepository
from src.use_case.port_manager import ReadOnlyField
from src.use_case.util.exceptions import IntMustBePositiveException, MissingRequiredFieldError
from src.use_case.util.mutation import is_set, Mutation
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class MutationRequest:
    """
    Mutation request for a switch. This represents the 'diff', that is going to be applied on the switch object.
    """
    switch_id: str = Mutation.NOT_SET
    ip_v4: str = Mutation.NOT_SET
    description: str = Mutation.NOT_SET
    community: str = Mutation.NOT_SET


class SwitchManager:
    def __init__(self, switch_repository: SwitchRepository):
        self.switch_repository = switch_repository

    def get_by_id(self, ctx, switch_id) -> Switch:
        """
        Get a switch in the database.
        User story: As an admin, I can get a switch by its id, so I can see all its informations.

        :raise SwitchNotFound
        """
        result, _ = self.switch_repository.search_switches_by(ctx, switch_id=switch_id)
        LOG.info("switch_get_by_id", extra=log_extra(ctx, switch_id=switch_id))

        if not result:
            raise SwitchNotFound()

        return result[0]

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, terms=None) -> (List[Switch], int):
        """
        Search switches in the database.
        User story: As an admin, I can search switches in the database, so I find the IP associated with a switch.

        :raise IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.switch_repository.search_switches_by(ctx, limit=limit, offset=offset, terms=terms)
        LOG.info("switch_search", extra=log_extra(ctx, terms=terms))

        return result, count

    def update(self, ctx, mutation_request: MutationRequest) -> None:
        """
        Update a switch in the database.
        User story: As an admin, I can update a switch in the database, so I update its community string.

        :raise SwitchNotFound
        """
        # Make sure the request is valid.
        _validate_mutation_request(mutation_request)

        if not is_set(mutation_request.switch_id):
            raise MissingRequiredFieldError('switch_id')

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if is_set(v)}
        try:
            self.switch_repository.update_switch(ctx, **fields_to_update)
            LOG.info("switch_update", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))

        except NotFoundError as e:
            raise SwitchNotFound() from e

    def create(self, ctx, mutation_request: MutationRequest) -> str:
        """
        Create a switch in the database.
        User story: As an admin, I can create a switch in the database, so I can add a new building.

        :return: the newly created switch ID

        :raise ReadOnlyField
        """
        # Make sure the request is valid.
        _validate_mutation_request(mutation_request)

        if is_set(mutation_request.switch_id):
            raise ReadOnlyField()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if is_set(v)}

        switch_id = self.switch_repository.create_switch(ctx, **fields_to_update)
        LOG.info("switch_create", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))

        return switch_id

    def delete(self, ctx, switch_id: str):
        """
        Delete a switch from the database.
        User story: As an admin, I can switch a port, so I can remove a old switch from the DB.

        :raise SwitchNotFound
        """
        try:
            self.switch_repository.delete_switch(ctx, switch_id)

        except NotFoundError as e:
            raise SwitchNotFound() from e


def _validate_mutation_request(req: MutationRequest):
    """
    Validate the fields that are set in a MutationRequest.
    """
    pass
