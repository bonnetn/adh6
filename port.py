from connexion import NoContent

PORTS = {
    0: {
        'portNumber': '1/0/4',
        'roomNumber': 5110,
        'switchID': 6,
    },
    1: {
        'portNumber': '1/0/3',
        'roomNumber': 5111,
        'switchID': 6,
    }
}


port_id = 42

def filterPort( limit=100, switchID=None, roomNumber=None ):
  res = []
  for k,v in PORTS.items():
      res += [ { 'portID':k, 'port':v } ]
  return res[:limit]

def createPort( switchID, body ):
  global port_id
  i = port_id
  port_id +=1
  PORTS[i] = body
  return "Created", 201, {'Location': '/switch/{}/port/{}'.format(switchID, i) }

def getPort( switchID, portID ):
  if portID not in PORTS:
    return "Not found", 404
  return PORTS[portID]

def updatePort( switchID, portID, body ):
  if portID not in PORTS:
    return "Not found", 404
  PORTS[portID] = body
  return NoContent, 204

def deletePort( switchID, portID ):
  if portID in PORTS:
    del PORTS[portID]
    return NoContent, 204
  else:
    return 'Not found', 404



  
