import json
from dataclasses import asdict
from typing import List

from src.entity.device import Device, DeviceType
from src.entity.room import Vlan
from src.log import LOG
from src.use_case.exceptions import IntMustBePositiveException, MemberNotFound
from src.use_case.interface.device_repository import DeviceRepository
from src.use_case.interface.ip_allocator import IPAllocator
from src.use_case.interface.member_repository import MemberRepository
from src.use_case.interface.room_repository import RoomRepository
from src.util.context import build_log_extra


class DeviceManager:
    def __init__(self,
                 member_storage: MemberRepository,
                 device_storage: DeviceRepository,
                 room_storage: RoomRepository,
                 ip_allocator: IPAllocator):
        self.device_storage = device_storage
        self.member_storage = member_storage
        self.room_storage = room_storage
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

        LOG.info("device_search", extra=build_log_extra(
            ctx,
            limit=limit,
            terms=terms,
        ))

        return result, count

    def update_or_create(self, ctx, mac_address: str, owner_username: str, connection_type):
        """
        Create/Update a device from the database.

        User story: As an admin, I can register a new device, so that a member can access internet with it.

        :return: True if the device was created, false otherwise.

        """

        # Make sure the provided owner username is valid.
        owner, _ = self.member_storage.search_member_by(ctx, username=owner_username)
        if not owner:
            raise MemberNotFound()

        # Allocate IP address.
        ip_v4_address = None
        ip_v6_address = None
        if connection_type == DeviceType.Wired:
            ip_v4_range, ip_v6_range = self._get_ip_range_for_user(ctx, owner_username)

            # TODO: Free addresses if cannot allocate.
            # TODO: Catch the exception if allocation failed.
            ip_v4_address = self.ip_allocator.allocate_ip_v4(ctx, ip_v4_range)
            ip_v6_address = self.ip_allocator.allocate_ip_v6(ctx, ip_v6_range)

        result, _ = self.device_storage.search_device_by(ctx, mac_address=mac_address)
        if not result:
            # No device with that MAC address, creating one...
            self.device_storage.create_device(ctx, mac_address=mac_address, owner_username=owner_username,
                                              connection_type=connection_type, ip_v4_address=ip_v4_address,
                                              ip_v6_address=ip_v6_address)

            LOG.info('device_create', extra=build_log_extra(
                ctx,
                username=owner_username,
                mac=mac_address,
                mutation=json.dumps(asdict(Device(
                    mac_address=mac_address,
                    owner_username=owner_username,
                    connection_type=connection_type,
                    ip_v4_address=ip_v4_address,
                    ip_v6_address=ip_v6_address,
                )), sort_keys=True)
            ))
            return True

        else:
            # A device exists, updating it.
            self.device_storage.update_device(ctx, mac_address=mac_address, owner_username=owner_username,
                                              connection_type=connection_type, ip_v4_address=ip_v4_address,
                                              ip_v6_address=ip_v6_address)
            LOG.info('device_update', extra=build_log_extra(
                ctx,
                username=owner_username,
                mac=mac_address,
                mutation=json.dumps(asdict(Device(
                    mac_address=mac_address,
                    owner_username=owner_username,
                    connection_type=connection_type,
                    ip_v4_address=ip_v4_address,
                    ip_v6_address=ip_v6_address,
                )), sort_keys=True)
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

        vlan: Vlan = result[0].vlan
        return vlan.ip_v4_range, vlan.ip_v6_range
