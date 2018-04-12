from connexion import NoContent
from sqlalchemy import or_
from adh.model.database import Database as db
from adh.model.models import Switch
from adh.exceptions import InvalidIPv4, SwitchNotFound


def switchExists(session, switchID):
    """ Return true if the switch exists """
    try:
        Switch.find(session, switchID)
    except SwitchNotFound:
        return False
    return True


def filterSwitch(limit=100, terms=None):
    """ [API] Filter the switch list """
    if limit < 0:
        return "Limit must be positive", 400
    result = db.get_db().get_session().query(Switch)
    # Filter by terms
    if terms:
        result = result.filter(or_(
            Switch.description.contains(terms),
            Switch.ip.contains(terms),
            Switch.communaute.contains(terms),
        ))
    result = result.limit(limit)  # Limit the number of matches
    result = result.all()

    # Convert the results into data suited for the API
    result = map(lambda x: {'switchID': x.id, 'switch': dict(x)}, result)
    result = list(result)  # Cast generator as list

    return result


def createSwitch(body):
    """ [API] Create a switch in the database """
    if "id" in body:
        return "You cannot set the id", 400
    session = db.get_db().get_session()
    try:
        switch = Switch.from_dict(session, body)
    except InvalidIPv4:
        return "Invalid IPv4", 400
    session.add(switch)
    session.commit()

    return NoContent, 201, {'Location': '/switch/{}'.format(switch.id)}


def getSwitch(switchID):
    """ [API] Get the specified switch from the database """
    session = db.get_db().get_session()
    try:
        return dict(Switch.find(session, switchID))
    except SwitchNotFound:
        return NoContent, 404


def updateSwitch(switchID, body):
    """ [API] Update the specified switch from the database """
    if "id" in body:
        return "You cannot update the id", 400

    session = db.get_db().get_session()
    if not switchExists(session, switchID):
        return NoContent, 404

    try:
        switch = Switch.from_dict(session, body)
        switch.id = switchID
    except InvalidIPv4:
        return "Invalid IPv4", 400

    session.merge(switch)
    session.commit()

    return NoContent, 204


def deleteSwitch(switchID):
    """ [API] Delete the specified switch from the database """
    session = db.get_db().get_session()

    try:
        switch = Switch.find(session, switchID)
    except SwitchNotFound:
        return NoContent, 404

    session.delete(switch)
    session.commit()

    return NoContent, 204
