from connexion import NoContent
from adh.model.database import Database as db
from adh.model import models
from dateutil import parser
import datetime
import sqlalchemy
from adh.exceptions.invalid_email import InvalidEmail


def dict_to_user(d):
    """ Converts a dictionnary to an User object """
    adh = models.Adherent(
        nom=d['lastName'],
        prenom=d['firstName'],
        mail=d['email'],
        login=d['username'],
    )
    if "departureDate" in d:
        adh.date_de_depart = parser.parse(d["departureDate"])
    if "associationMode" in d:
        adh.mode_association = parser.parse(d["associationMode"])
    if "comment" in d:
        adh.commentaires = d["comment"]
    return adh


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

    roomNumber = body["user"]["roomNumber"]
    if roomNumber and not roomExists(roomNumber):
        return "Room not found", 400

    if adherentExists(username):
        s = db.get_db().get_session()
        q = s.query(models.Adherent)
        q = q.filter(models.Adherent.login == username)

        userDict = body["user"]

        a = q.one()
        a.nom = userDict['lastName']
        a.prenom = userDict['firstName']
        try:
            a.mail = userDict['email']
        except InvalidEmail:
            s.rollback()
            return "Invalid email", 400
        a.login = userDict['username']

        if roomNumber:
            q2 = s.query(models.Chambre)
            q2 = q2.filter(models.Chambre.numero == roomNumber)
            c = q2.one()
            a.chambre = c

        if "departureDate" in userDict:
            a.date_de_depart = parser.parse(userDict["departureDate"])
        if "associationMode" in userDict:
            a.mode_association = parser.parse(userDict["associationMode"])
        if "comment" in userDict:
            a.commentaires = userDict["comment"]

        s.commit()
        return 'Updated', 204
    else:
        s = db.get_db().get_session()
        try:
            a = dict_to_user(body["user"])
        except InvalidEmail:
            s.rollback()
            return "Invalid email", 400
        if roomNumber:
            q2 = s.query(models.Chambre)
            q2 = q2.filter(models.Chambre.numero == roomNumber)
            c = q2.one()
            a.chambre = c
        s.add(a)
        s.commit()
        return 'Created', 201


def addMembership(username, body):
    """ [API] Add a membership record in the database """

    s = db.get_db().get_session()

    try:
        q = s.query(models.Adherent)
        q = q.filter(models.Adherent.login == username)
        a = q.one()
    except sqlalchemy.orm.exc.NoResultFound:
        return "Not found", 404

    start = parser.parse(body["start"])
    duration = body["duration"]
    end = start + datetime.timedelta(days=duration)

    s.add(models.Adhesion(
        adherent=a,
        depart=start,
        fin=end
    ))

    s.commit()
    return NoContent, 200, {'Location': 'test'}
