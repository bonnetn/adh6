from connexion import NoContent
from itertools import islice
from store import get_db


def findInDevice(user, terms):
    txt = ""
    txt += user["mac"] + " "
    txt += user["ipAddress"] + " "
    txt += user["ipv6Address"] + " "
    return txt.lower().find(terms.lower()) != -1


def filterDevice(limit=100, username=None, terms=None):
    DEVICES = get_db()["DEVICES"]
    all_devices = list(DEVICES.values())

    if username != None:
        all_devices = filter(lambda x: x["username"] == username, all_devices)

    if terms != None:
        all_devices = filter(lambda x: findInDevice(x, terms), all_devices)

    return list(islice(all_devices, limit))


def putDevice(macAddress, body):
    DEVICES = get_db()["DEVICES"]
    if macAddress in DEVICES:
        retVal = ("Updated", 204)
    else:
        retVal = ("Created", 201)

    if macAddress != body["mac"]:
        del DEVICES[macAddress]

    body["ipAddress"] = "127.0.0.1"
    body["ipv6Address"] = "::1/128"

    DEVICES[body["mac"]] = body
    return retVal


def getDevice(macAddress):
    DEVICES = get_db()["DEVICES"]
    if macAddress in DEVICES:
        return DEVICES[macAddress]
    else:
        return 'Not found', 404


def deleteDevice(macAddress):
    DEVICES = get_db()["DEVICES"]
    if macAddress in DEVICES:
        del DEVICES[macAddress]
        return NoContent, 204
    else:
        return 'Not found', 404
