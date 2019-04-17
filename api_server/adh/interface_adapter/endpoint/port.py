import json
import logging

from connexion import NoContent
from flask import g
from sqlalchemy import or_

from adh.auth import auth_regular_admin, auth_super_admin
from adh.exceptions import RoomNotFound, SwitchNotFound, PortNotFound
from adh.model.models import Port, Chambre, Switch
from adh.util.session_decorator import require_sql


@require_sql
@auth_regular_admin
def search(limit=100, offset=0,
                switchID=None, roomNumber=None, terms=None):
    """ [API] Filter the port list according to some criteria """
    if limit < 0:
        return 'Limit must be a positive number', 400

    s = g.session
    q = s.query(Port)
    if switchID:
        q = q.join(Switch)
        q = q.filter(Switch.id == switchID)
    if roomNumber:
        q = q.join(Chambre)
        q = q.filter(Chambre.numero == roomNumber)
    if terms:
        q = q.filter(or_(
            Port.numero.contains(terms),
            Port.oid.contains(terms),
        ))

    count = q.count()
    q = q.order_by(Port.switch_id.asc(), Port.numero.asc())
    q = q.offset(offset)
    q = q.limit(limit)
    result = q.all()

    result = map(dict, result)
    result = list(result)
    headers = {
        'access-control-expose-headers': 'X-Total-Count',
        'X-Total-Count': str(count)
    }
    logging.info("%s fetched the port list", g.admin.login)
    return result, 200, headers


@require_sql
@auth_super_admin
def post(body):
    """ [API] Create a port in the database """

    s = g.session
    try:
        port = Port.from_dict(s, body)
    except SwitchNotFound:
        return "Switch not found", 400
    except RoomNotFound:
        return "Room not found", 400

    s.add(port)
    s.flush()  # Needed to fetch the port.id
    headers = {'Location': '/port/{}'.format(port.id)}
    logging.info("%s created the port\n%s",
                 g.admin.login, json.dumps(body, sort_keys=True))
    return NoContent, 200, headers


@require_sql
@auth_regular_admin
def get(port_id):
    """ [API] Get a port from the database """
    s = g.session
    try:
        result = Port.find(s, port_id)
    except PortNotFound:
        return NoContent, 404

    result = dict(result)
    logging.info("%s fetched the port /port/%d",
                 g.admin.login, port_id)
    return result, 200


@require_sql
@auth_super_admin
def put(port_id, body):
    """ [API] Update a port in the database """

    s = g.session

    try:
        new_port = Port.from_dict(s, body)
    except SwitchNotFound:
        return "Switch not found", 400

    try:
        new_port.id = Port.find(s, port_id).id
    except PortNotFound:
        return "Port not found", 404

    s.merge(new_port)

    logging.info("%s updated the port /port/%d\n%s",
                 g.admin.login, port_id, json.dumps(body, sort_keys=True))
    return NoContent, 204


@require_sql
@auth_super_admin
def delete(port_id):
    """ [API] Delete a port from the database """
    s = g.session
    try:
        s.delete(Port.find(s, port_id))
    except PortNotFound:
        return NoContent, 404
    logging.info("%s deleted the port /port/%d",
                 g.admin.login, port_id)
    return NoContent, 204

@auth_regular_admin
def get_state(switchID, port_id):
    return NoContent, 200, True


@auth_regular_admin
def put_state(switchID, port_id, state):
    return NoContent, 200


@auth_regular_admin
def get_vlan(switchID, port_id):
    return NoContent, 200, 42


@auth_regular_admin
def put_vlan(switchID, port_id, vlan):
    return NoContent, 204

@auth_regular_admin
def get_mab(port_id):
    return False, 200

@auth_regular_admin
def put_mab(port_id, mab):
    return NoContent, 204
