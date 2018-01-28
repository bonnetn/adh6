from connexion import NoContent
from model.database import Database as db
from model import models


def user_to_dict(adh):
    return {
        'email': adh.mail,
        'firstName': adh.prenom,
        'lastName': adh.nom,
        'username': adh.login,
        'departureDate': adh.date_de_depart,
        'comment': adh.commentaires,
        'associationMode': adh.mode_association,
        'roomNumber': adh.chambre_id
    }


def filterUser(limit=100, terms=None, roomNumber=None):
    s = db.get_db().get_session()

    q = s.query(models.Adherent)
    # if username:
    #     q = q.filter(models.Portable.adherent == target)
    # if terms:
    #     q = q.filter(
    #         (models.Portable.mac.contains(terms)) |
    #         False  # TODO: compare on username ?
    #     )
    q = q.limit(limit)
    r = q.all()
    return list(map(user_to_dict, r)), 200


def getUser(username):
    return ''


def deleteUser(username):
    return NoContent, 204


def putUser(username, body):
    return 'Created', 201


def addMembership(username, body):
    return NoContent, 200, {'Location': 'test'}
