from connexion import NoContent

SWITCHES = {
    0: {
        'description' : "Switch U1",
        'ip'          : "192.168.102.11",
        'community'   : "tototo"
    },
    1: {
        'description' : "Switch U2",
        'ip'          : "192.168.102.12",
        'community'   : "tututu"
    }
    2: {
        'description' : "Switch-local",
        'ip'          : "192.168.102.12",
        'community'   : "tirelinpimpon"
    },
        
}
switch_id = 42

def filterSwitch( limit=100 ):
  res = []
  for k,v in SWITCHES.items():
      res += [{ 'switchID': k, 'switch': v }]
  return res[:limit]

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

