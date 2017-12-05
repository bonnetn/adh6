from connexion import NoContent
ROOMS = {
    1111 : {
        'description' : "Chambre 1111",
        'roomNumber'  : 1111,
        'phone'       : 0,
        'vlan'        : 41
    },
    1234 : {
        'description' : "Chambre 1234",
        'roomNumber'  : 1234,
        'phone'       : 0,
        'vlan'        : 41
    }
}

def filterRoom( limit=100 ):
  return list(ROOMS.values())[:limit]

def putRoom( roomNumber, body ):
        if roomNumber in ROOMS:
                retVal = 'Updated', 204
        else:
                retVal = 'Created', 201
        ROOMS[roomNumber] = body
        return retVal

def getRoom( roomNumber ):
        if roomNumber not in ROOMS:
                return "Room not found", 404
        return ROOMS[roomNumber]

def deleteRoom( roomNumber ):
        if roomNumber in ROOMS:
                del ROOMS[roomNumber]
                return NoContent, 204
        else:
                return 'Not found', 404
