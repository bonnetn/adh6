from connexion import NoContent
from sqlalchemy import or_
from adh.exceptions import RoomNotFound, VlanNotFound
from adh.model.database import Database as db
from adh.model.models import Chambre


def roomExists(session, roomNumber):
    """ Returns true if the room exists in the database """
    try:
        Chambre.find(session, roomNumber)
    except RoomNotFound:
        return False
    return True


def filterRoom(limit=100, offset=0, terms=None):
    """ [API] Filter the list of the rooms """
    if limit < 0:
        return "Limit must be a positive integer", 400
    s = db.get_db().get_session()
    q = s.query(Chambre)
    if terms:
        q = q.filter(or_(
            Chambre.telephone.contains(terms),
            Chambre.description.contains(terms),
        ))
    count = q.count()
    q = q.order_by(Chambre.id.asc())
    q = q.offset(offset)
    q = q.limit(limit)
    result = q.all()
    result = map(dict, result)
    result = list(result)
    headers = {
        'access-control-expose-headers': 'X-Total-Count',
        'X-Total-Count': str(count)
    }
    return result, 200, headers


def putRoom(roomNumber, body):
    """ [API] Update/create a room in the database """
    s = db.get_db().get_session()

    try:
        new_room = Chambre.from_dict(s, body)
    except VlanNotFound:
        return "Vlan not found", 400
    room_exists = roomExists(s, roomNumber)

    if room_exists:
        new_room.id = Chambre.find(s, roomNumber).id

    s.merge(new_room)
    s.commit()

    if room_exists:
        return NoContent, 204
    else:
        return NoContent, 201


def getRoom(roomNumber):
    """ [API] Get the room specified """
    s = db.get_db().get_session()
    try:
        return dict(Chambre.find(s, roomNumber)), 200
    except RoomNotFound:
        return NoContent, 404


def deleteRoom(roomNumber):
    """ [API] Delete room from the database """
    s = db.get_db().get_session()
    try:
        s.delete(Chambre.find(s, roomNumber))
    except RoomNotFound:
        return NoContent, 404

    s.commit()
    return NoContent, 204
