from connexion import NoContent
from store import get_db
from sqlalchemy import or_
import sqlalchemy.orm.exc
from model.database import db
from model.models import Switch
import logging


def toDict(s):
    """ Transforms a Switch object to dictionary """
    return {
        'description': s.description,
        'ip': s.ip,
        'community': s.communaute
    }


def fromDict(body):
    """ Transforms a dictionary to Switch object """
    return Switch(
        description=body['description'],
        ip=body['ip'],
        communaute=body['community']
    )


def filterSwitch(limit=100, terms=None):
    try:
        result = db.get_session().query(Switch)
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
        result = map(lambda x: {'switchID': x.id, 'switch': toDict(x)}, result)
        result = list(result)  # Cast generator as list

        return result

    except Exception as e:
        logging.error('Could not filterSwitch(...). Exception: {}'
                      .format(e))
        return NoContent, 500


def createSwitch(body):
    try:
        switch = fromDict(body)
        session = db.get_session()
        session.add(switch)
        session.commit()

        return NoContent, 201, {'Location': '/switch/{}'.format(switch.id)}

    except Exception as e:
        logging.error('Could not createSwitch(...). Exception: {}'
                      .format(e))
        return NoContent, 500


def getSwitch(switchID):
    try:
        result = db.get_session().query(Switch)
        result = result.filter(Switch.id == switchID)
        result = result.one()
        result = toDict(result)

        return result

    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    except Exception as e:
        logging.error('Could not getSwitch({}). Exception: {}'
                      .format(switchID, e))
        return NoContent, 500


def updateSwitch(switchID, body):
    SWITCHES = get_db()["SWITCHES"]
    if switchID not in SWITCHES:
        return "Not found", 404
    SWITCHES[switchID] = body
    SWITCHES[switchID]["_id"] = switchID
    return NoContent, 204


def deleteSwitch(switchID):
    SWITCHES = get_db()["SWITCHES"]
    if switchID in SWITCHES:
        del SWITCHES[switchID]
        return NoContent, 204
    else:
        return 'Switch not found', 404
