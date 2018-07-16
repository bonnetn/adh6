import logging
import json
from connexion import NoContent
from sqlalchemy import or_
from adh.exceptions import RoomNotFound, VlanNotFound
from adh.model.database import Database as Db
from adh.model.models import Chambre
from adh.auth import auth_simple_user, auth_admin


def room_exists(session, room_number):
    """ Returns true if the room exists in the database """
    try:
        Chambre.find(session, room_number)
    except RoomNotFound:
        return False
    return True


@auth_simple_user
def filter_room(admin, limit=100, offset=0, terms=None):
    """ [API] Filter the list of the rooms """
    if limit < 0:
        return "Limit must be a positive integer", 400
    s = Db.get_db().get_session()
    q = s.query(Chambre)
    if terms:
        q = q.filter(or_(
            Chambre.telephone.contains(terms),
            Chambre.description.contains(terms),
        ))
    count = q.count()
    q = q.order_by(Chambre.id.asc())
    q = q.offset(offset)
    q = q.limit(limit)
    result = q.all()
    result = map(dict, result)
    result = list(result)
    headers = {
        'access-control-expose-headers': 'X-Total-Count',
        'X-Total-Count': str(count)
    }

    logging.info("%s fetched the room list", admin.login)
    return result, 200, headers


@auth_admin
def put_room(admin, room_number, body):
    """ [API] Update/create a room in the database """
    s = Db.get_db().get_session()

    try:
        new_room = Chambre.from_dict(s, body)
    except VlanNotFound:
        return "Vlan not found", 400
    exists = room_exists(s, room_number)

    if exists:
        new_room.id = Chambre.find(s, room_number).id

    s.merge(new_room)
    s.commit()

    if exists:
        logging.info("%s updated the room %d\n%s",
                     admin.login, room_number, json.dumps(body, sort_keys=True))
        return NoContent, 204
    else:
        logging.info("%s created the room %d\n%s",
                     admin.login, room_number, json.dumps(body, sort_keys=True))
        return NoContent, 201


@auth_simple_user
def get_room(admin, room_number):
    """ [API] Get the room specified """
    s = Db.get_db().get_session()
    try:
        logging.info("%s fetched the room %d", admin.login, room_number)
        return dict(Chambre.find(s, room_number)), 200
    except RoomNotFound:
        return NoContent, 404


@auth_admin
def delete_room(admin, room_number):
    """ [API] Delete room from the database """
    s = Db.get_db().get_session()
    try:
        s.delete(Chambre.find(s, room_number))
    except RoomNotFound:
        return NoContent, 404

    s.commit()
    logging.info("%s deleted the room %d", admin.login, room_number)
    return NoContent, 204
