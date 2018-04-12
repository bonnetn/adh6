from connexion import NoContent
from adh.model.database import Database as db
from adh.model import models
from adh.util.date import string_to_date
from adh.exceptions.invalid_email import InvalidEmail
import datetime
import sqlalchemy

# MERGE
# FAIRE FONCTION STATIQUE POUR FIND ROOMS
# merge totues les exceptions dans 1 fichier


def findRoom(roomNumber):
    if not roomNumber:
        return None
    s = db.get_db().get_session()
    q = s.query(models.Chambre)
    q = q.filter(models.Chambre.numero == roomNumber)
    return q.one()


def fromDict(d):
    return models.Adherent(
        mail=d.get("email"),
        prenom=d.get("firstName"),
        nom=d.get("lastName"),
        login=d.get("username"),
        date_de_depart=string_to_date(d.get('departureDate')),
        commentaires=d.get('comment'),
        mode_association=string_to_date(d.get('associationMode')),
        chambre=findRoom(d.get("roomNumber")),
    )


def filterUser(limit=100, terms=None, roomNumber=None):
    """ [API] Filter the list of users from the the database """
    if limit < 0:
        return "Limit must be positive", 400

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
    return list(map(dict, r)), 200


def getUser(username):
    """ [API] Get the specified user from the database """
    s = db.get_db().get_session()
    q = s.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)
    try:
        return dict(q.one())
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404


def deleteUser(username):
    """ [API] Delete the specified User from the database """
    s = db.get_db().get_session()
    q = s.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)
    try:
        s.delete(q.one())
        s.commit()
        return NoContent, 204
    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404


def adherentExists(username):
    """ Returns true if the user exists """
    session = db.get_db().get_session()
    q = session.query(models.Adherent)
    q = q.filter(models.Adherent.login == username)

    return session.query(q.exists()).scalar()


def roomExists(roomNumber):
    """ Returns true if the user exists """
    session = db.get_db().get_session()
    q = session.query(models.Chambre)
    q = q.filter(models.Chambre.numero == roomNumber)

    return session.query(q.exists()).scalar()


def putUser(username, body):
    """ [API] Create/Update user from the database """

    s = db.get_db().get_session()
    update = adherentExists(username)
    try:
        s.merge(fromDict(body))
    except ValueError:
        return "String must not be empty", 400
    except InvalidEmail:
        return "Invalid email", 400
    except sqlalchemy.orm.exc.NoResultFound:
        return "No room found", 400

    s.commit()
    if update:
        return NoContent, 204
    else:
        return NoContent, 201


def addMembership(username, body):
    """ [API] Add a membership record in the database """

    s = db.get_db().get_session()

    try:
        q = s.query(models.Adherent)
        q = q.filter(models.Adherent.login == username)
        a = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return "Not found", 404

    start = string_to_date(body["start"])
    duration = body["duration"]
    end = start + datetime.timedelta(days=duration)

    s.add(models.Adhesion(
        adherent=a,
        depart=start,
        fin=end
    ))

    s.commit()
    return NoContent, 200, {'Location': 'test'}
