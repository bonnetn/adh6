from connexion import NoContent
from itertools import islice

PORTS = {
    0: {
        'portNumber': '1/0/4',
        'roomNumber': 1234,
        'switchID': 1,
    },
    1: {
        'portNumber': '1/0/3',
        'roomNumber': 1111,
        'switchID': 2,
    },
    2: {
        'portNumber': '1/0/7',
        'roomNumber': 1111,
        'switchID': 3,
    },
    3: {
        'portNumber': '1/0/8',
        'roomNumber': 1234,
        'switchID': 1,
    }
}

for k,v in PORTS.items():
    v["_id"] = k


port_id = 42

def findInPort( port, terms ):
    txt = ""
    txt += port["portNumber"] + " "
    txt += str(port["roomNumber"]) + " "
    return txt.lower().find( terms.lower() ) != -1

def filterPort( limit=100, switchID=None, roomNumber=None, terms=None ):
    all_ports = list(PORTS.values())
    
    if switchID != None:
        all_ports = filter( lambda x: x["switchID"] == switchID, all_ports )

    if roomNumber != None:
        all_ports = filter( lambda x: x["roomNumber"] == roomNumber, all_ports )

    if terms != None:
        all_ports = filter( lambda x: findInPort( x, terms ), all_ports )
    
    all_ports = islice(all_ports, limit)
    all_ports = map( lambda x: { 'portID': x["_id"], 'switchID':x['switchID'],
        'port':x}, all_ports)
    return list(all_ports)


def createPort( switchID, body ):
  global port_id
  i = port_id
  port_id +=1
  PORTS[i] = body
  PORTS[i]["_id"] =i
  return "Created", 201, {'Location': '/switch/{}/port/{}'.format(switchID, i) }

def getPort( switchID, portID ):
  if portID not in PORTS:
    return "Not found", 404
  return PORTS[portID]

def updatePort( switchID, portID, body ):
  if portID not in PORTS:
    return "Not found", 404
  PORTS[portID] = body
  PORTS[portID]["_id"] = portID
  return NoContent, 204

def deletePort( switchID, portID ):
  if portID in PORTS:
    del PORTS[portID]
    return NoContent, 204
  else:
    return 'Not found', 404



  
