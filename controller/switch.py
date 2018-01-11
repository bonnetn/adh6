from connexion import NoContent
from itertools import islice

SWITCHES = {
    1: {
        'description' : "Switch U1",
        'ip'          : "192.168.102.11",
        'community'   : "tototo"
    },
    2: {
        'description' : "Switch U2",
        'ip'          : "192.168.102.12",
        'community'   : "tututu"
    },
    3: {
        'description' : "Switch-local",
        'ip'          : "192.168.102.12",
        'community'   : "tirelinpimpon"
    },
}

for k,v in SWITCHES.items():
    v["_id"] = k

switch_id = 42

def findInSwitch( switch, terms ):
    txt = ""
    txt += switch["description"] + " "
    txt += switch["ip"] + " "
    txt += switch["community"] + " " # lol search on community :D
    return txt.lower().find( terms.lower() ) != -1


def filterSwitch( limit=100, terms=None ):
  all_switches = list(SWITCHES.values())
  
  if terms != None:
      all_switches = filter( lambda x: findInSwitch(x, terms), all_switches )
  
  all_switches = islice(all_switches, limit)

  all_switches = map( lambda x: {"switchID": x["_id"], "switch": x },
          all_switches)

  return list(all_switches)

def createSwitch( body ):
  global switch_id
  i = switch_id
  switch_id += 1
  SWITCHES[i] = body
  SWITCHES[i]["_id"] = i
  return NoContent, 201, { 'Location':'/switch/{}'.format(i) }

def getSwitch( switchID ):
  if switchID not in SWITCHES:
    return "Not found", 404
  return SWITCHES[switchID]

def updateSwitch( switchID, body ):
  if switchID not in SWITCHES:
    return "Not found", 404
  SWITCHES[switchID] = body
  SWITCHES[switchID]["_id"] = switchID
  return NoContent, 204

def deleteSwitch( switchID ):
  if switchID in SWITCHES:
    del SWITCHES[switchID]
    return NoContent, 204
  else:
    return 'Switch not found', 404

