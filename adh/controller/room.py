from connexion import NoContent
from sqlalchemy import or_
from adh.model.database import Database as db
from adh.model.models import Chambre
import sqlalchemy


def fromDict(d):
    """ Converts a dictionnary into an actual Port object """
    adh = Chambre(
        numero=d['roomNumber'],
    )
    if "description" in d:
        adh.description = d["description"]
    if "phone" in d:
        adh.telephone = d["phone"]
    # if "vlan" in d:
    #     adh.vlan = d["comment"]
    return adh


def filterRoom(limit=100, terms=None):
    """ [API] Filter the list of the rooms """
    s = db.get_db().get_session()
    q = s.query(Chambre)
    if terms:
        q = q.filter(or_(
            Chambre.telephone.contains(terms),
            Chambre.description.contains(terms),
        ))
    q = q.limit(limit)
    result = q.all()
    result = map(dict, result)
    result = list(result)
    return result, 200


def roomExists(roomNumber):
    """ Returns true if the room exists in the database """
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)

    return s.query(q.exists()).scalar()


def putRoom(roomNumber, body):
    """ [API] Update/create a room in the database """
    roomDict = body

    if roomExists(roomNumber):
        s = db.get_db().get_session()
        q = s.query(Chambre)
        q = q.filter(Chambre.numero == roomNumber)
        a = q.one()
        a.numero = roomDict['roomNumber']

        if "description" in roomDict:
            a.description = roomDict["description"]
        if "phone" in roomDict:
            a.telephone = roomDict["phone"]
        """
        TODO
        if "vlan" in roomDict:
            a.vlan = roomDict["vlan"]
        """
        s.commit()
        return 'Updated', 204
    else:
        s = db.get_db().get_session()
        a = fromDict(body)
        s.add(a)
        print(a)
        s.commit()
        return "Created", 201


def getRoom(roomNumber):
    """ [API] Get the room specified """
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)
    try:
        return dict(q.one()), 200
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404


def deleteRoom(roomNumber):
    """ [API] Delete room from the database """
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)
    try:
        s.delete(q.one())
        s.commit()
        return NoContent, 204
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404
