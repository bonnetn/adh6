from connexion import NoContent

SWITCHES = {}
switch_id = 0

def filterSwitch( limit=100 ):
  return list(SWITCHES.values())[:limit]

def createSwitch( body ):
  global switch_id
  i = switch_id
  switch_id += 1
  SWITCHES[i] = body
  return NoContent, 201, { 'Location':'/switch/{}'.format(i) }

def getSwitch( switchID ):
  if switchID not in SWITCHES:
    return "Not found", 404
  return SWITCHES[switchID]

def updateSwitch( switchID, body ):
  if switchID not in SWITCHES:
    return "Not found", 404
  SWITCHES[switchID] = body
  return NoContent, 204

def deleteSwitch( switchID ):
  if switchID in SWITCHES:
    del SWITCHES[switchID]
    return NoContent, 204
  else:
    return 'Switch not found', 404

