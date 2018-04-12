from connexion import NoContent
from adh.model.database import Database as db
from adh.model.models import Adherent, Chambre, Adhesion
from adh.util.date import string_to_date
from adh.exceptions import InvalidEmail, RoomNotFound, UserNotFound
import datetime
import sqlalchemy

# FAIRE FONCTION STATIQUE POUR FIND ROOMS


def adherentExists(session, username):
    """ Returns true if the user exists """
    q = session.query(Adherent)
    q = q.filter(Adherent.login == username)

    return session.query(q.exists()).scalar()


def filterUser(limit=100, terms=None, roomNumber=None):
    """ [API] Filter the list of users from the the database """
    if limit < 0:
        return "Limit must be positive", 400

    s = db.get_db().get_session()

    q = s.query(Adherent)
    if roomNumber:
        try:
            q2 = s.query(Chambre)
            q2 = q2.filter(Chambre.numero == roomNumber)
            result = q2.one()
        except sqlalchemy.orm.exc.NoResultFound:
            return [], 200

        q = q.filter(Adherent.chambre == result)
    if terms:
        q = q.filter(
            (Adherent.nom.contains(terms)) |
            (Adherent.prenom.contains(terms)) |
            (Adherent.mail.contains(terms)) |
            (Adherent.login.contains(terms)) |
            (Adherent.commentaires.contains(terms))
        )
    q = q.limit(limit)
    r = q.all()
    return list(map(dict, r)), 200


def getUser(username):
    """ [API] Get the specified user from the database """
    s = db.get_db().get_session()
    try:
        return dict(Adherent.find(s, username))
    except UserNotFound:
        return NoContent, 404


def deleteUser(username):
    """ [API] Delete the specified User from the database """
    s = db.get_db().get_session()
    try:
        s.delete(Adherent.find(s, username))
        s.commit()
        return NoContent, 204
    except UserNotFound:
        return NoContent, 404


def putUser(username, body):
    """ [API] Create/Update user from the database """

    s = db.get_db().get_session()
    update = adherentExists(s, username)
    try:
        s.merge(Adherent.from_dict(s, body))
    except ValueError:
        return "String must not be empty", 400
    except InvalidEmail:
        return "Invalid email", 400
    except RoomNotFound:
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
        q = s.query(Adherent)
        q = q.filter(Adherent.login == username)
        a = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return "Not found", 404

    start = string_to_date(body["start"])
    duration = body["duration"]
    end = start + datetime.timedelta(days=duration)

    s.add(Adhesion(
        adherent=a,
        depart=start,
        fin=end
    ))

    s.commit()
    return NoContent, 200, {'Location': 'test'}
