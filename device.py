from connexion import NoContent

DEVICES = {}

def putDevice( macAddress, body ):
  if macAddress in DEVICES:
    retVal = ("Updated", 204)
  else:
    retVal = ("Created", 201)
  
  DEVICES[macAddress] = body
  return retVal

def getDevice( macAddress ):
  if macAddress in DEVICES:
    return DEVICES[ macAddress ]
  else:
    return 'Not found', 404

def deleteDevice( macAddress ):
  if macAddress in DEVICES:
    del DEVICES[macAddress]
    return NoContent, 204
  else:
    return 'Not found', 404


def filterDevice( limit=100, username=None ):

  all_devices = list(DEVICES.values())
  if username == None:
    return all_devices[:limit]
  
  return list(filter( lambda x: x["username"]==username, all_devices))[:limit]


  
