from connexion import NoContent


USERS = {
		"coroller": {
			"email":"stevan.coroller@telecom-em.eu",
			"firstName":"Stevan",
			"lastName":"Coroller",
			"username":"coroller",
			"comment":"Desauthent pour routeur",
			"roomNumber": 1111,
			"departureDate": "2017-12-13 00:00:00",
			"associationMode": "2017-01-01 00:00:00"
		},
		"cherre_r": {
			"email":"romain.cherre@telecom-em.eu",
			"firstName":"Romain",
			"lastName":"Cherré",
			"username":"cherre_r",
			"comment":"Mdr",
			"roomNumber": 1111,
			"departureDate": "2017-12-13 00:00:00",
			"associationMode": "2017-01-01 00:00:00"
		},
		"coutelou": {
			"email":"thomas.coutelou@telecom-sudparis.eu",
			"firstName":"Thomas",
			"lastName":"Coutelou",
			"username":"coutelou",
			"comment":"Desauthent pour PS4",
			"roomNumber": 1234,
			"departureDate": "2017-12-13 00:00:00",
			"associationMode": "2017-01-01 00:00:00"
		}

}

def findInUser( user, terms ):
  if terms == None:
    return False
  s = ""
  s += user["email" ] + " "
  s += user["firstName" ] + " "
  s += user["lastName" ] + " "
  s += user["username" ] + " "
  s += str(user["roomNumber" ])
  return s.lower().find(terms.lower()) != -1


def filterUser( limit=100, terms=None, roomNumber=None ):
  all_users = list(USERS.values())
  if terms == None and roomNumber == None:
    return all_users[:limit]
  
  return list(filter( lambda x: \
    findInUser(x, terms) or x["roomNumber"] == roomNumber, \
    all_users))[:limit]

def getUser( username ):
	if username not in USERS:
		return "User not found", 404
	return USERS[ username ]

def deleteUser( username ):
	if username in USERS:
		del USERS[username]
		return NoContent, 204
	else:
		return 'Not found', 404

def putUser( username, body ):
	if username in USERS:
		retVal = ("Updated", 204)
	else:
		retVal = ("Created", 201)
	USERS[username] = body["user"]
	return retVal
	
