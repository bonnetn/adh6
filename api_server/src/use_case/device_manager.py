# coding=utf-8
import json
from dataclasses import asdict, dataclass
from typing import List, Optional

from src.entity.device import Device, DeviceType
from src.use_case.interface.device_repository import DeviceRepository
from src.use_case.interface.ip_allocator import IPAllocator, NoMoreIPAvailableException
from src.use_case.interface.member_repository import MemberRepository, NotFoundError
from src.use_case.interface.room_repository import RoomRepository
from src.use_case.interface.vlan_repository import VLANRepository
from src.use_case.util.exceptions import IntMustBePositiveException, MemberNotFound, IPAllocationFailedError, \
    InvalidMACAddress, InvalidIPAddress, DeviceNotFound
from src.use_case.util.mutation import Mutation, is_set
from src.util.checks import is_mac_address, is_ip_v4, is_ip_v6
from src.util.context import log_extra
from src.util.log import LOG


@dataclass
class MutationRequest(Device):
    """
    Mutation request for a device. This represents the 'diff', that is going to be applied on the device object.
    """
    mac_address: str = Mutation.NOT_SET
    owner_username: str = Mutation.NOT_SET
    connection_type: str = Mutation.NOT_SET
    ip_v4_address: Optional[str] = Mutation.NOT_SET
    ip_v6_address: Optional[str] = Mutation.NOT_SET


class DeviceManager:
    def __init__(self,
                 member_storage: MemberRepository,
                 device_storage: DeviceRepository,
                 room_storage: RoomRepository,
                 vlan_storage: VLANRepository,
                 ip_allocator: IPAllocator):
        self.device_storage = device_storage
        self.member_storage = member_storage
        self.room_storage = room_storage
        self.vlan_storage = vlan_storage
        self.ip_allocator = ip_allocator

    def search(self, ctx, limit=100, offset=0, username=None, terms=None) -> (List[Device], int):
        """
        Search a device in the database.

        User story: As an admin, I can search all the devices, so I can see the device list of a member.

        :raises IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositiveException('limit')

        if offset < 0:
            raise IntMustBePositiveException('offset')

        result, count = self.device_storage.search_device_by(ctx, limit=limit, offset=offset, username=username,
                                                             terms=terms)

        LOG.info("device_search", extra=log_extra(
            ctx,
            limit=limit,
            terms=terms,
        ))

        return result, count

    def get_by_mac_address(self, ctx, mac_address: str) -> Device:
        """
        Get a device from the database.

        User story: As an admin, I can get a device, so I can see its information such as IP address.

        :raises DeviceNotFound
        """
        result, count = self.device_storage.search_device_by(ctx, mac_address=mac_address)
        if not result:
            raise DeviceNotFound()

        LOG.info("device_get_by_username", extra=log_extra(
            ctx,
            mac_address=mac_address,
        ))

        return result[0]

    def delete(self, ctx, mac_address: str):
        """
        Delete a device from the database.

        User story: As an admin, I delete a device, so I can remove a device from a user profile.

        :raises DeviceNotFound
        """
        try:
            self.device_storage.delete_device(ctx, mac_address=mac_address)
        except NotFoundError as e:
            raise DeviceNotFound() from e

        LOG.info("device_delete", extra=log_extra(
            ctx,
            mac=mac_address,
        ))

    def update_or_create(self, ctx, mac_address: str, req: MutationRequest):
        """
        Create/Update a device from the database.

        User story: As an admin, I can register a new device, so that a member can access internet with it.

        :return: True if the device was created, false otherwise.

        :raises MemberNotFound
        :raises IPAllocationFailedError
        :raises InvalidMACAddress
        :raises InvalidIPAddress
        """

        if not is_set(req.mac_address):
            req.mac_address = mac_address

        _validate_mutation_request(req)

        # Make sure the provided owner username is valid.
        owner, _ = self.member_storage.search_member_by(ctx, username=req.owner_username)
        if not owner:
            raise MemberNotFound()

        # Allocate IP address.
        if req.connection_type == DeviceType.Wired:
            ip_v4_range, ip_v6_range = self._get_ip_range_for_user(ctx, req.owner_username)

            # TODO: Free addresses if cannot allocate.
            try:
                if not is_set(req.ip_v4_address) and ip_v4_range:
                    req.ip_v4_address = self.ip_allocator.allocate_ip_v4(ctx, ip_v4_range)
                if not is_set(req.ip_v6_address) and ip_v6_range:
                    req.ip_v6_address = self.ip_allocator.allocate_ip_v6(ctx, ip_v6_range)

            except NoMoreIPAvailableException as e:
                raise IPAllocationFailedError() from e

        fields = {k: v if is_set(v) else None for k, v in asdict(req).items()}
        result, _ = self.device_storage.search_device_by(ctx, mac_address=mac_address)

        req.ip_v4_address = req.ip_v4_address or 'En Attente'
        req.ip_v6_address = req.ip_v6_address or 'En Attente'
        if not result:
            # No device with that MAC address, creating one...
            self.device_storage.create_device(ctx, **fields)

            LOG.info('device_create', extra=log_extra(
                ctx,
                username=req.owner_username,
                mac=mac_address,
                mutation=json.dumps(fields, sort_keys=True)
            ))
            return True

        else:
            # A device exists, updating it.

            # The following will never throw DeviceNotFound since we check beforehand.
            self.device_storage.update_device(ctx, mac_address, **fields)

            LOG.info('device_update', extra=log_extra(
                ctx,
                username=req.owner_username,
                mac=mac_address,
                mutation=json.dumps(fields, sort_keys=True)
            ))
            return False

    def _get_ip_range_for_user(self, ctx, username) -> (str, str):
        """
        Return the IP range that that a user should be assigned to.
        :return: IPv4 range and IPv6 range of the user
        """
        result, count = self.room_storage.search_room_by(ctx, owner_username=username)
        if not result:
            return None, None

        vlan = self.vlan_storage.get_vlan(ctx, result[0].vlan_number)
        return vlan.ip_v4_range, vlan.ip_v6_range


def _validate_mutation_request(req: MutationRequest):
    if not is_mac_address(req.mac_address):
        raise InvalidMACAddress()

    if is_set(req.ip_v4_address) and not is_ip_v4(req.ip_v4_address):
        raise InvalidIPAddress()

    if is_set(req.ip_v6_address) and not is_ip_v6(req.ip_v6_address):
        raise InvalidIPAddress()
