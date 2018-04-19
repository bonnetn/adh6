from connexion import NoContent
from adh.model.database import Database as db
from adh.model.models import Adherent, Chambre, Adhesion
from adh.util.date import string_to_date
from adh.exceptions import InvalidEmail, RoomNotFound, UserNotFound
import datetime
import sqlalchemy


def adherentExists(session, username):
    """ Returns true if the user exists """
    try:
        Adherent.find(session, username)
    except UserNotFound:
        return False
    return True


def filterUser(limit=100, offset=0, terms=None, roomNumber=None):
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
    q = q.offset(offset)
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

    try:
        new_user = Adherent.from_dict(s, body)
    except ValueError:
        return "String must not be empty", 400
    except InvalidEmail:
        return "Invalid email", 400
    except RoomNotFound:
        return "No room found", 400

    update = adherentExists(s, username)
    if update:
        new_user.id = Adherent.find(s, username).id

    s.merge(new_user)
    s.commit()
    if update:
        return NoContent, 204
    else:
        return NoContent, 201


def addMembership(username, body):
    """ [API] Add a membership record in the database """

    s = db.get_db().get_session()

    start = string_to_date(body["start"])
    end = None
    if start and "duration" in body:
        duration = body["duration"]
        end = start + datetime.timedelta(days=duration)

    try:
        s.add(Adhesion(
            adherent=Adherent.find(s, username),
            depart=start,
            fin=end
        ))
    except UserNotFound:
        return NoContent, 404

    s.commit()
    return NoContent, 200, {'Location': 'test'}  # TODO: finish that!
