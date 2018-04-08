from connexion import NoContent
from model.database import Database as db
from sqlalchemy import or_
from model.models import Port
import sqlalchemy.orm.exc


def toDict(port):
    return {
        "port": dict(port),
        "switchID": port.switch.id,
        "portID": port.id
    }


def fromDict(d):
    return Port(
        chambre_id=d["roomNumber"],
        switch_id=d["switchID"],
        numero=d["portNumber"]
    )


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
    port = fromDict(body)
    session = db.get_db().get_session()
    session.add(port)
    session.commit()
    headers = {
        'Location': '/switch/{}/port/{}'.format(port.switch_id, port.id)
    }
    return NoContent, 200, headers


def getPort(switchID, portID):
    q = db.get_db().get_session().query(Port)
    q = q.filter(Port.id == portID)
    try:
        result = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    result = toDict(result)
    result = list(result)
    return result, 200


def updatePort(switchID, portID, body):
    s = db.get_db().get_session()
    q = s.query(Port)
    q = q.filter(Port.id == portID)
    try:
        port = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    port.chambre_id = body["roomNumber"]
    port.switch_id = body["switchID"]
    port.numero = body["portNumber"]
    s.commit()

    return NoContent, 204


def deletePort(switchID, portID):
    try:
        session = db.get_db().get_session()
        port = session.query(Port).filter(Port.id == portID).one()
        session.delete(port)

        session.commit()

        return NoContent, 204

    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404
