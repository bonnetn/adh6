from connexion import NoContent
from model.database import Database as db
from model import models
from dateutil import parser
import datetime
import sqlalchemy


def user_to_dict(adh):
    d = {
        'email': adh.mail,
        'firstName': adh.prenom,
        'lastName': adh.nom,
        'username': adh.login,
        'departureDate': adh.date_de_depart,
        'comment': adh.commentaires,
        'associationMode': adh.mode_association,
    }
    if adh.chambre:
        d['roomNumber'] = adh.chambre.numero
    return d


def dict_to_user(d):
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


def putUser(username, body):
    if adherentExists(username):
        s = db.get_db().get_session()
        q = s.query(models.Adherent)
        q = q.filter(models.Adherent.login == username)

        userDict = body["user"]

        a = q.one()
        a.nom = userDict['lastName']
        a.prenom = userDict['firstName']
        a.mail = userDict['email']
        a.login = userDict['username']

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
        a = dict_to_user(body["user"])
        s.add(a)
        s.commit()
        return 'Created', 201


def addMembership(username, body):
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
