from connexion import NoContent
from itertools import islice
from store import get_db


def findInRoom(room, terms):
    txt = ""
    txt += room["description"] + " "
    txt += str(room["roomNumber"]) + " "
    txt += str(room["phone"]) + " "

    return txt.lower().find(terms.lower()) != -1


def filterRoom(limit=100, terms=None):
    all_rooms = list(get_db()["ROOMS"].values())

    if terms != None:
        all_rooms = filter(lambda x: findInRoom(x, terms), all_rooms)

    return list(islice(all_rooms, limit))


def putRoom(roomNumber, body):
    ROOMS = get_db()["ROOMS"]
    if roomNumber in ROOMS:
        retVal = 'Updated', 204
    else:
        retVal = 'Created', 201
    ROOMS[roomNumber] = body
    return retVal


def getRoom(roomNumber):
    ROOMS = get_db()["ROOMS"]
    if roomNumber not in ROOMS:
        return "Room not found", 404
    return ROOMS[roomNumber]


def deleteRoom(roomNumber):
    ROOMS = get_db()["ROOMS"]
    if roomNumber in ROOMS:
        del ROOMS[roomNumber]
        return NoContent, 204
    else:
        return 'Not found', 404
