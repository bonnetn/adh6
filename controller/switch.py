from connexion import NoContent
from sqlalchemy import or_
import sqlalchemy.orm.exc
from model.database import Database as db
from model.models import Switch
import logging
from controller import checks


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
        result = map(lambda x: {'switchID': x.id, 'switch': toDict(x)}, result)
        result = list(result)  # Cast generator as list

        return result

    except Exception as e:
        logging.error('Could not filterSwitch(...). Exception: {}'
                      .format(e))
        return NoContent, 500


def createSwitch(body):
    if not checks.isIPv4(body['ip']):
        return NoContent, 400
    try:
        switch = fromDict(body)
        session = db.get_db().get_session()
        session.add(switch)
        session.commit()

        return NoContent, 201, {'Location': '/switch/{}'.format(switch.id)}

    except Exception as e:
        logging.error('Could not createSwitch(...). Exception: {}'
                      .format(e))
        return NoContent, 500


def getSwitch(switchID):
    try:
        result = db.get_db().get_session().query(Switch)
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
    if not checks.isIPv4(body['ip']):
        return NoContent, 400
    try:
        session = db.get_db().get_session()

        # Don't update if the Switch does not exists
        q = session.query(Switch).filter(Switch.id == switchID)
        if not session.query(q.exists()).scalar():
            return NoContent, 404

        switch = fromDict(body)
        switch.id = switchID
        session.merge(switch)

        session.commit()

        return NoContent, 204

    except Exception as e:
        logging.error('Could not updateSwitch({}). Exception: {}'
                      .format(switchID, e))
        return NoContent, 500


def deleteSwitch(switchID):
    try:
        session = db.get_db().get_session()
        # Get the switch to delete
        switch = session.query(Switch).filter(Switch.id == switchID).one()
        session.delete(switch)

        session.commit()

        return NoContent, 204

    except sqlalchemy.orm.exc.NoResultFound:
        return NoContent, 404

    except Exception as e:
        logging.error('Could not deleteSwitch({}). Exception: {}'
                      .format(switchID, e))
        return NoContent, 500
