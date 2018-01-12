from connexion import NoContent
from datetime import datetime
from itertools import islice
from store import get_db


def findInUser(user, terms):
    s = ""
    s += user["firstName"] + " "
    s += user["lastName"] + " "
    s += user["username"] + " "
    s += str(user["roomNumber"])
    return s.lower().find(terms.lower()) != -1


def filterUser(limit=100, terms=None, roomNumber=None):
    USERS = get_db()['USERS']
    all_users = list(USERS.values())

    if terms != None:
        all_users = filter(lambda x: findInUser(x, terms), all_users)

    if roomNumber != None:
        all_users = filter(lambda x: x["roomNumber"] == roomNumber, all_users)

    return list(islice(all_users, limit))


def getUser(username):
    USERS = get_db()['USERS']
    if username not in USERS:
        return "User not found", 404
    return USERS[username]


def deleteUser(username):
    USERS = get_db()['USERS']
    if username in USERS:
        del USERS[username]
        return NoContent, 204
    else:
        return 'Not found', 404


def putUser(username, body):
    USERS = get_db()['USERS']
    if username in USERS:
        retVal = ("Updated", 204)
    else:
        retVal = ("Created", 201)
    USERS[username] = body["user"]
    return retVal


def addMembership(username, body):
    USERS = get_db()['USERS']
    if username not in USERS:
        return "Not found", 404

    if "start" not in body:
        start = datetime.now().isoformat()
    else:
        start = body["start"]

    USERS[username]["departureDate"] = start

    # TODO: return the right header
    # TODO: return 201 instead of 200
    return NoContent, 200, {"Location": "test"}
