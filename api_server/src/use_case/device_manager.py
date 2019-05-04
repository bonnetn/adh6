# coding=utf-8
import json
from dataclasses import asdict, dataclass
from typing import List, Optional

from src.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.entity.device import Device, DeviceType, ALL_DEVICE_TYPES
from src.exceptions import InvalidMACAddress, MissingRequiredField, InvalidIPv4, InvalidIPv6
from src.exceptions import NoMoreIPAvailableException, MemberNotFound, DeviceNotFound, IntMustBePositive, \
    IPAllocationFailedError
from src.use_case.interface.device_repository import DeviceRepository
from src.use_case.interface.ip_allocator import IPAllocator
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.room_repository import RoomRepository
from src.use_case.interface.vlan_repository import VLANRepository
from src.util.context import log_extra
from src.util.log import LOG
from src.util.validator import is_mac_address, is_ip_v4, is_ip_v6, is_empty


@dataclass
class MutationRequest(Device):
    """
    Mutation request for a device. This represents the 'diff', that is going to be applied on the device object.
    """
    mac_address: str
    owner_username: str
    connection_type: str
    ip_v4_address: Optional[str]
    ip_v6_address: Optional[str]

    def validate(self):
        # MAC ADDRESS:
        if not is_mac_address(self.mac_address):
            raise InvalidMACAddress()

        # OWNER USERNAME:
        if is_empty(self.owner_username):
            raise MissingRequiredField('owner_username')

        # CONNECTION TYPE:
        if is_empty(self.connection_type):
            raise MissingRequiredField('connection_type')

        if self.connection_type not in ALL_DEVICE_TYPES:
            raise ValueError('invalid connection type')

        # IP_V4_ADDRESS:
        if self.ip_v4_address is not None and not is_ip_v4(self.ip_v4_address):
            raise InvalidIPv4(self.ip_v4_address)

        # IP_V6_ADDRESS:
        if self.ip_v6_address is not None and not is_ip_v6(self.ip_v6_address):
            raise InvalidIPv6(self.ip_v6_address)


class DeviceManager:
    def __init__(self,
                 member_repository: MemberRepository,
                 device_repository: DeviceRepository,
                 room_repository: RoomRepository,
                 vlan_repository: VLANRepository,
                 ip_allocator: IPAllocator):
        self.device_repository = device_repository
        self.member_repository = member_repository
        self.room_repository = room_repository
        self.vlan_repository = vlan_repository
        self.ip_allocator = ip_allocator

    def search(self, ctx, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET, username=None, terms=None) -> (List[Device], int):
        """
        Search a device in the database.

        User story: As an admin, I can search all the devices, so I can see the device list of a member.

        :raise IntMustBePositiveException
        """
        if limit < 0:
            raise IntMustBePositive('limit')

        if offset < 0:
            raise IntMustBePositive('offset')

        result, count = self.device_repository.search_device_by(ctx, limit=limit, offset=offset, username=username,
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

        :raise DeviceNotFound
        """
        result, count = self.device_repository.search_device_by(ctx, mac_address=mac_address)
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

        :raise DeviceNotFound
        """
        self.device_repository.delete_device(ctx, mac_address=mac_address)

        LOG.info("device_delete", extra=log_extra(
            ctx,
            mac=mac_address,
        ))

    def update_or_create(self, ctx, mac_address: str, req: MutationRequest):
        """
        Create/Update a device from the database.

        User story: As an admin, I can register a new device, so that a member can access internet with it.

        :return: True if the device was created, false otherwise.

        :raise MemberNotFound
        :raise IPAllocationFailedError
        :raise InvalidMACAddress
        :raise InvalidIPAddress
        """

        req.validate()

        # Make sure the provided owner username is valid.
        owner, _ = self.member_repository.search_member_by(ctx, username=req.owner_username)
        if not owner:
            raise MemberNotFound()

        # Allocate IP address.
        if req.connection_type == DeviceType.Wired:
            ip_v4_range, ip_v6_range = self._get_ip_range_for_user(ctx, req.owner_username)

            # TODO: Free addresses if cannot allocate.
            try:
                if req.ip_v4_address is None and ip_v4_range:
                    req.ip_v4_address = self.ip_allocator.allocate_ip_v4(ctx, ip_v4_range)

                if req.ip_v6_address is None and ip_v6_range:
                    req.ip_v6_address = self.ip_allocator.allocate_ip_v6(ctx, ip_v6_range)

            except NoMoreIPAvailableException as e:
                raise IPAllocationFailedError() from e

        fields = {k: v for k, v in asdict(req).items()}
        result, _ = self.device_repository.search_device_by(ctx, mac_address=mac_address)
        if not result:
            # No device with that MAC address, creating one...
            self.device_repository.create_device(ctx, **fields)

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
            self.device_repository.update_device(ctx, mac_address, **fields)

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
        result, count = self.room_repository.search_room_by(ctx, owner_username=username)
        if not result:
            return None, None

        vlan = self.vlan_repository.get_vlan(ctx, result[0].vlan_number)
        return vlan.ip_v4_range, vlan.ip_v6_range
