from connexion import NoContent
from sqlalchemy import or_
from model.database import Database as db
from model.models import Chambre


def toDict(r):
    return {
        "roomNumber": r.numero,
        "vlan": r.vlan.numero,
        "phone": r.telephone,
        "description": r.description,
    }


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


def putRoom(roomNumber, body):
    s = db.get_db().get_session()
    q = s.query(Chambre)
    q = q.filter(Chambre.numero == roomNumber)
    return NoContent, 500


def getRoom(roomNumber):
    return NoContent, 500


def deleteRoom(roomNumber):
    return NoContent, 500
