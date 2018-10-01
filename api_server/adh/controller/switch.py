import json
import logging

from connexion import NoContent
from flask import g
from sqlalchemy import or_

from adh.auth import auth_regular_admin, auth_super_admin
from adh.exceptions import InvalidIPv4, SwitchNotFound
from adh.model.models import Switch
from adh.util.session_decorator import require_sql


def switch_exists(session, switchID):
    """ Return true if the switch exists """
    try:
        Switch.find(session, switchID)
    except SwitchNotFound:
        return False
    return True


@require_sql
@auth_regular_admin
def filter_switch(limit=100, offset=0, terms=None):
    """ [API] Filter the switch list """
    if limit < 0:
        return "Limit must be positive", 400
    q = g.session.query(Switch)
    # Filter by terms
    if terms:
        q = q.filter(or_(
            Switch.description.contains(terms),
            Switch.ip.contains(terms),
            Switch.communaute.contains(terms),
        ))
    count = q.count()
    q = q.order_by(Switch.description.asc())
    q = q.offset(offset)
    q = q.limit(limit)  # Limit the number of matches
    q = q.all()

    # Convert the qs into data suited for the API
    q = map(lambda x: {'switchID': x.id, 'switch': dict(x)}, q)
    result = list(q)  # Cast generator as list

    headers = {
        'access-control-expose-headers': 'X-Total-Count',
        'X-Total-Count': str(count)
    }
    logging.info("%s fetched the switch list", g.admin.login)
    return result, 200, headers


@require_sql
@auth_super_admin
def create_switch(body):
    """ [API] Create a switch in the database """
    if "id" in body:
        return "You cannot set the id", 400
    s = g.session
    try:
        switch = Switch.from_dict(s, body)
    except InvalidIPv4:
        return "Invalid IPv4", 400
    s.add(switch)

    logging.info("%s created a switch\n%s", g.admin.login, json.dumps(body,
                                                                      sort_keys=True))
    s.flush()  # Needed to set the switch.id
    return NoContent, 201, {'Location': '/switch/{}'.format(switch.id)}


@require_sql
@auth_regular_admin
def get_switch(switchID):
    """ [API] Get the specified switch from the database """
    s = g.session
    try:
        logging.info("%s fetched the switch %d", g.admin.login, switchID)
        return dict(Switch.find(s, switchID))
    except SwitchNotFound:
        return NoContent, 404


@require_sql
@auth_super_admin
def update_switch(switchID, body):
    """ [API] Update the specified switch from the database """
    if "id" in body:
        return "You cannot update the id", 400

    s = g.session
    if not switch_exists(s, switchID):
        return NoContent, 404

    try:
        switch = Switch.from_dict(s, body)
        switch.id = switchID
    except InvalidIPv4:
        return "Invalid IPv4", 400

    s.merge(switch)

    logging.info("%s updated the switch %d\n%s",
                 g.admin.login, switchID, json.dumps(body, sort_keys=True))
    return NoContent, 204


@require_sql
@auth_super_admin
def delete_switch(switchID):
    """ [API] Delete the specified switch from the database """
    s = g.session

    try:
        switch = Switch.find(s, switchID)
    except SwitchNotFound:
        return NoContent, 404

    s.delete(switch)

    logging.info("%s deleted the switch %d", g.admin.login, switchID)
    return NoContent, 204
