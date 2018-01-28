from connexion import NoContent
from model.database import Database as db
from model import models
import sqlalchemy


def user_to_dict(adh):
    return {
        'email': adh.mail,
        'firstName': adh.prenom,
        'lastName': adh.nom,
        'username': adh.login,
        'departureDate': adh.date_de_depart,
        'comment': adh.commentaires,
        'associationMode': adh.mode_association,
        'roomNumber': adh.chambre.numero
    }


def filterUser(limit=100, terms=None, roomNumber=None):
    s = db.get_db().get_session()

    q = s.query(models.Adherent)
    if roomNumber:
        try:
            q2 = s.query(models.Chambre)
            q2 = q2.filter(models.Chambre.numero == roomNumber)
            result = q2.one()
        except sqlalchemy.orm.exc.NoResultFound:
            return [], 200

        q = q.filter(models.Adherent.chambre == result)
    if terms:
        q = q.filter(
            (models.Adherent.nom.contains(terms)) |
            (models.Adherent.prenom.contains(terms)) |
            (models.Adherent.mail.contains(terms)) |
            (models.Adherent.login.contains(terms)) |
            (models.Adherent.commentaires.contains(terms))
        )
    q = q.limit(limit)
    r = q.all()
    return list(map(user_to_dict, r)), 200


def getUser(username):
    s = db.get_db().get_session()
    q = s.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)
    try:
        return user_to_dict(q.one())
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404


def deleteUser(username):
    s = db.get_db().get_session()
    q = s.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)
    try:
        s.delete(q.one())
        return NoContent, 204
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404


def putUser(username, body):
    return 'Created', 201


def addMembership(username, body):
    return NoContent, 200, {'Location': 'test'}
