from connexion import NoContent  


def getPortStatus(switchID, portID):
    return 204, NoContent, True

def setPortStatus(switchID, portID, state):
    return 200, NoContent

def getPortVlan(switchID, portID):
    return 200, NoContent, 42

def setPortVlan(switchID, portID, vlan):
    return 204, NoContent
