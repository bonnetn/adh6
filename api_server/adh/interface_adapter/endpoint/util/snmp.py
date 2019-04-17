from pysnmp.hlapi import (
    setCmd, SnmpEngine, CommunityData, ObjectType, ObjectIdentity, Integer,
    UdpTransportTarget, ContextData, getCmd
)


class SNMPError(Exception):
    def __init__(self, value):
        self.value = value


class SNMPManager:

    def __init__(self, server, secret, port=161):
        self.server = server
        self.secret = secret
        self.port = port

    def change_value(self, req, oid, value):

        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                setCmd(
                    SnmpEngine(), CommunityData(
                        self.secret), UdpTransportTarget(
                        (self.server, self.port)), ContextData(), ObjectType(
                        ObjectIdentity(
                            req + str(oid)), Integer(value))), )
        except Exception:
            raise
        else:
            if errorIndication:
                return SNMPError(errorIndication)
            elif errorStatus:
                return SNMPError(errorStatus)
            else:
                if len(varBinds) == 1:
                    return varBinds[0][1]
                else:
                    raise SNMPError("Multiple MIB variables returned.")

    def make_request(self, req, oid):
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(self.secret),
                       UdpTransportTarget((self.server, self.port)),
                       ContextData(),
                       ObjectType(ObjectIdentity(req + str(oid)))),
            )
        except Exception:
            raise
        else:

            if errorIndication:
                return SNMPError(errorIndication)
            elif errorStatus:
                return SNMPError(errorStatus)
            else:
                if len(varBinds) == 1:
                    return varBinds[0][1]
                else:
                    raise SNMPError("Multiple MIB variables returned.")
