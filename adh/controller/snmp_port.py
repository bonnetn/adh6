from connexion import NoContent
from adh.auth import auth_simple_user


@auth_simple_user
def getPortStatus(switchID, portID):
    return 204, NoContent, True


@auth_simple_user
def setPortStatus(switchID, portID, state):
    return 200, NoContent


@auth_simple_user
def getPortVlan(switchID, portID):
    return 200, NoContent, 42


@auth_simple_user
def setPortVlan(switchID, portID, vlan):
    return 204, NoContent
