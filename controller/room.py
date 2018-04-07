from connexion import NoContent
from sqlalchemy import or_
from model.database import Database as db
from model.models import Chambre
import sqlalchemy


def toDict(r):
    return {
        "roomNumber": r.numero,
        "vlan": 42,
        "phone": r.telephone,
        "description": r.description,
    }


def fromDict(d):
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
    s = db.get_db().get_session()
    q = s.query(Chambre)
    if terms:
        q = q.filter(or_(
            Chambre.telephone.contains(terms),
            Chambre.description.contains(terms),
        ))
    q.limit(limit)
    result = q.all()
    result = map(toDict, result)
    result = list(result)
    return result, 200


def roomExists(roomNumber):
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)

    return s.query(q.exists()).scalar()


def putRoom(roomNumber, body):
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
    return NoContent, 500


def deleteRoom(roomNumber):
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)
    try:
        s.delete(q.one())
        s.commit()
        return NoContent, 204
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404
