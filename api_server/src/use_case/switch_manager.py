import json
from dataclasses import dataclass, asdict
from typing import List

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.switch import Switch
from src.exceptions import SwitchNotFound, IntMustBePositiveException, MissingRequiredField, \
    InvalidIPv4
from src.use_case.interface.switch_repository import SwitchRepository
from src.util.context import log_extra
from src.util.log import LOG
from src.util.validator import is_ip_v4


@dataclass
class MutationRequest:
    """
    Mutation request for a switch. This represents the 'diff', that is going to be applied on the switch object.
    """
    ip_v4: str
    description: str
    community: str

    def validate(self):
        """
        Validate the fields that are set in a MutationRequest.
        """
        if self.ip_v4 is None:
            raise MissingRequiredField('ip_v4')

        if not is_ip_v4(self.ip_v4):
            raise InvalidIPv4(self.ip_v4)

        if self.description is None:
            raise MissingRequiredField('description')

        if self.community is None:
            raise MissingRequiredField('community')


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

    def update(self, ctx, switch_id: str, mutation_request: MutationRequest) -> None:
        """
        Update a switch in the database.
        User story: As an admin, I can update a switch in the database, so I update its community string.

        :raise SwitchNotFound
        """
        # Make sure the request is valid.
        mutation_request.validate()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}
        try:
            self.switch_repository.update_switch(ctx, switch_id=switch_id, **fields_to_update)
            LOG.info("switch_update", extra=log_extra(ctx, mutation=json.dumps(fields_to_update, sort_keys=True)))

        except SwitchNotFound as e:
            raise SwitchNotFound() from e

    def create(self, ctx, mutation_request: MutationRequest) -> str:
        """
        Create a switch in the database.
        User story: As an admin, I can create a switch in the database, so I can add a new building.

        :return: the newly created switch ID

        :raise ReadOnlyField
        """
        # Make sure the request is valid.
        mutation_request.validate()

        fields_to_update = asdict(mutation_request)
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}

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

        except SwitchNotFound as e:
            raise SwitchNotFound() from e
