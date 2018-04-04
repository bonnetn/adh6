from connexion import NoContent
from model.database import Database as db
from sqlalchemy import or_
from model.models import Port


def toDict(port):
    return {
        "port": {
            "roomNumber": port.chambre_id,
            "switchID": port.switch.id,
            "portNumber": port.numero,
        },
        "switchID": port.switch.id,
        "portID": port.id
    }


def filterPort(limit=100, switchID=None, roomNumber=None, terms=None):

    q = db.get_db().get_session().query(Port)
    if switchID:
        q = q.filter(Port.switch_id == switchID)
    if roomNumber:
        q = q.filter(Port.chambre_id == roomNumber)
    if terms:
        q = q.filter(or_(
            Port.numero.contains(terms),
            Port.oid.contains(terms),
        ))
    q = q.limit(limit)
    result = q.all()

    result = map(toDict, result)
    result = list(result)
    return result, 200


def createPort(switchID, body):
    return NoContent, 500


def getPort(switchID, portID):
    return NoContent, 500


def updatePort(switchID, portID, body):
    return NoContent, 500


def deletePort(switchID, portID):
    return NoContent, 500
