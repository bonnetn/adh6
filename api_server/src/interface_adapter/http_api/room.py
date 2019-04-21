import json
import logging

from connexion import NoContent
from flask import g
from sqlalchemy import or_

from src.exceptions import RoomNotFound, VlanNotFound
from src.interface_adapter.http_api.decorator.auth import auth_regular_admin, auth_super_admin
from src.interface_adapter.sql.model.models import Chambre
from src.interface_adapter.http_api.decorator.sql_session import require_sql


def room_exists(session, roomNumber):
    """ Returns true if the room exists in the database """
    try:
        Chambre.find(session, roomNumber)
    except RoomNotFound:
        return False
    return True


@require_sql
@auth_regular_admin
def search(limit=100, offset=0, terms=None):
    """ [API] Filter the list of the rooms """
    if limit < 0:
        return "Limit must be a positive integer", 400
    s = g.session
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

    logging.info("%s fetched the room list", g.admin.login)
    return result, 200, headers


@require_sql
@auth_super_admin
def put(roomNumber, body):
    """ [API] Update/create a room in the database """
    s = g.session

    try:
        new_room = Chambre.from_dict(s, body)
    except VlanNotFound:
        return "Vlan not found", 400
    exists = room_exists(s, roomNumber)

    if exists:
        new_room.id = Chambre.find(s, roomNumber).id

    s.merge(new_room)

    if exists:
        logging.info("%s updated the room %d\n%s",
                     g.admin.login, roomNumber, json.dumps(body, sort_keys=True))
        return NoContent, 204
    else:
        logging.info("%s created the room %d\n%s",
                     g.admin.login, roomNumber, json.dumps(body, sort_keys=True))
        return NoContent, 201


@require_sql
@auth_regular_admin
def get(roomNumber):
    """ [API] Get the room specified """
    s = g.session
    try:
        logging.info("%s fetched the room %d", g.admin.login, roomNumber)
        return dict(Chambre.find(s, roomNumber)), 200
    except RoomNotFound:
        return NoContent, 404


@require_sql
@auth_super_admin
def delete(roomNumber):
    """ [API] Delete room from the database """
    s = g.session
    try:
        s.delete(Chambre.find(s, roomNumber))
    except RoomNotFound:
        return NoContent, 404

    logging.info("%s deleted the room %d", g.admin.login, roomNumber)
    return NoContent, 204
