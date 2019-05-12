# coding=utf-8
"""
Implements everything related to SNMP-related actions
"""
from src.entity.port import Port
from src.entity.switch import Switch
from src.exceptions import NetworkManagerReadError
from src.interface_adapter.snmp.util.snmp_helper import get_SNMP_value
from src.use_case.interface.switch_network_manager import SwitchNetworkManager
from src.util.context import log_extra
from src.util.log import LOG


class SwitchSNMPNetworkManager(SwitchNetworkManager):

    def get_port_status(self, ctx, switch: Switch = None, port: Port = None) -> bool:
        """
        Retrieve the status of a port.

        :raise PortNotFound
        """

        #LOG.debug("switch_network_manager_get_port_status_called", extra=log_extra(ctx, port=port))

        if switch is None:
            raise NetworkManagerReadError("SNMP read error: switch object was None")
        if port is None:
            raise NetworkManagerReadError("SNMP read error: port object was None")

        try:
            return get_SNMP_value(switch.community, switch.ip_v4, 'IF-MIB', 'ifAdminStatus', port.switch_info.oid)
        except NetworkManagerReadError:
            raise

    def update_port_status(self, ctx, switch: Switch = None, port: Port = None, status=None) -> None:
        """
        Update the status of a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    def get_port_vlan(self, ctx, switch: Switch = None, port: Port = None) -> int:
        """
        Get the VLAN assigned to a port.

        :raise PortNotFound
        """

        #LOG.debug("switch_network_manager_get_port_vlan_called", extra=log_extra(ctx, port=port))

        if switch is None:
            raise NetworkManagerReadError("SNMP read error: switch object was None")
        if port is None:
            raise NetworkManagerReadError("SNMP read error: port object was None")

        try:
            return get_SNMP_value(switch.community, switch.ip_v4, 'CISCO-VLAN-MEMBERSHIP-MIB', 'vmVlan',
                                  port.switch_info.oid)
        except NetworkManagerReadError:
            raise

    def update_port_vlan(self, ctx, switch: Switch = None, port: Port = None, vlan=None) -> None:
        """
        Update the VLAN assigned to a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover

    def get_port_mab(self, ctx, switch: Switch = None, port: Port = None) -> bool:
        """
        Retrieve whether MAB is active on a port.

        :raise PortNotFound
        """

        LOG.debug("switch_network_manager_get_port_mab_called", extra=log_extra(port))

        if switch is None:
            raise NetworkManagerReadError("SNMP read error: switch object was None")
        if port is None:
            raise NetworkManagerReadError("SNMP read error: port object was None")

        try:
            return get_SNMP_value(switch.community, switch.ip_v4, 'CISCO-MAC-AUTH-BYPASS-MIB', 'cmabIfAuthEnabled',
                                  port.switch_info.oid)
        except NetworkManagerReadError:
            raise

    def update_port_mab(self, ctx, switch: Switch = None, port: Port = None, mab=None) -> None:
        """
        Update whether MAB should be active on a port.

        :raise PortNotFound
        """
        pass  # pragma: no cover
