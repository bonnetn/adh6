from connexion import NoContent

PORTS = {
    0: {
        'portNumber': '1/0/4',
        'roomNumber': 1234,
        'switchID': 0,
    },
    1: {
        'portNumber': '1/0/3',
        'roomNumber': 1111,
        'switchID': 0,
    },
    2: {
        'portNumber': '1/0/7',
        'roomNumber': 1111,
        'switchID': 1,
    },
    3: {
        'portNumber': '1/0/8',
        'roomNumber': 1234,
        'switchID': 1,
    }
}


port_id = 42

def filterPort( limit=100, switchID=None, roomNumber=None ):
  res = []
  for k,v in PORTS.items():
      # ugly: to improve...
      if (switchID and switchID == v['switchID']) or (roomNumber and roomNumber == v['roomNumber']) or (not roomNumber and not switchID):
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



  
