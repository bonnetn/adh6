from connexion import NoContent
from adh.model.database import Database as db
from sqlalchemy import or_
from adh.model.models import Port, Switch
from adh.exceptions import RoomNotFound, SwitchNotFound
import sqlalchemy.orm.exc


def findSwitch(switchID):
    """ Returns a switch if it exists, None otherwise """
    s = db.get_db().get_session()
    q2 = s.query(Switch)
    q2 = q2.filter(Switch.id == switchID)
    try:
        return q2.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def filterPort(limit=100, switchID=None, roomNumber=None, terms=None):
    """ [API] Filter the port list according to some criteria """
    if limit < 0:
        return 'Limit must be a positive number', 400

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

    result = map(dict, result)
    result = list(result)
    return result, 200


def createPort(switchID, body):
    """ [API] Create a port in the database """

    session = db.get_db().get_session()
    try:
        port = Port.from_dict(session, body)
    except SwitchNotFound:
        return "Switch not found", 400
    except RoomNotFound:
        return "Room not found", 400
    switch = findSwitch(body["switchID"])
    if not switch:
        return 'Switch does not exist', 400
    port.switch = switch
    session.add(port)
    session.commit()
    headers = {
        'Location': '/switch/{}/port/{}'.format(port.switch_id, port.id)
    }
    return NoContent, 200, headers


def getPort(switchID, portID):
    """ [API] Get a port from the database """
    q = db.get_db().get_session().query(Port)
    q = q.filter(Port.id == portID)
    try:
        result = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    result = dict(result)
    result = list(result)
    return result, 200


def updatePort(switchID, portID, body):
    """ [API] Update a port in the database """

    switch = findSwitch(body["switchID"])
    if not switch:
        return 'Switch does not exist', 400

    s = db.get_db().get_session()
    q = s.query(Port)
    q = q.filter(Port.id == portID)
    try:
        port = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    port.chambre_id = body["roomNumber"]
    port.switch = switch
    port.numero = body["portNumber"]
    s.commit()

    return NoContent, 204


def deletePort(switchID, portID):
    """ [API] Delete a port from the database """
    try:
        session = db.get_db().get_session()
        port = session.query(Port).filter(Port.id == portID).one()
        session.delete(port)

        session.commit()

        return NoContent, 204

    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404
