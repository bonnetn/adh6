from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd, \
    setCmd

from src.exceptions import NetworkManagerReadError


def get_SNMP_value(community, ip, MIB, obj, oid):
    """ Performs an SNMP RO request and retrieves the respons """
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(MIB, obj, oid))
               ))
    if errorIndication:
        raise NetworkManagerReadError("SNMP read error:" + str(errorIndication))
    elif errorStatus:
        raise NetworkManagerReadError('SNMP read error: %s at %s' % (errorStatus.prettyPrint(),
                                                                     errorIndex and varBinds[int(errorIndex) - 1][
                                                                         0] or '?'))
    else:
        if len(varBinds) > 1:
            raise NetworkManagerReadError("SNMP read error: too many values in response")

        return varBinds[0][1].prettyPrint()


def set_SNMP_value(community, ip, MIB, obj, oid, value):
    """ Performs an SNMP RW request and sets the given oid to the given value """
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(MIB, obj, oid))
               ))
    if errorIndication:
        raise NetworkManagerReadError("SNMP read error:" + str(errorIndication))
    elif errorStatus:
        raise NetworkManagerReadError('SNMP read error: %s at %s' % (errorStatus.prettyPrint(),
                                                                     errorIndex and varBinds[int(errorIndex) - 1][
                                                                         0] or '?'))
    else:
        if len(varBinds) > 1:
            raise NetworkManagerReadError("SNMP read error: too many values in response")

        return varBinds[0][1].prettyPrint()
