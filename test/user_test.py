from controller import user
import unittest

u = {
  'email'           : "kevin@cazal.eu",
  'firstName'       : "Kévin",
  'lastName'        : "Cazal",
  'username'        : "cazal_k",
  'departureDate'  	: "2017-12-12 00:00:00",
  'comment'	        : "Desauth pour routeur",
  'associationMode'	: "2016-05-02 12:30:52",
  'roomNumber'     	: "7701"
}

u2 = {
  'email'           : "test@test.com",
  'firstName'       : "Nicolas",
  'lastName'        : "Bonnet",
  'username'        : "bonnet_n",
  'departureDate'  	: "2018-12-12 00:00:00",
  'comment'	        : "Desauth pour PS4",
  'associationMode'	: "2016-05-02 12:30:52",
  'roomNumber'     	: "7218"
}

user_req = { \
        'user':u, \
        'password':"test" \
      }

user_req2 = { \
        'user':u2, \
        'password':"tototo" \
      }


class TestUser(unittest.TestCase):

    def test(self):
      resultString, resultCode = user.put(u["username"], user_req)
      self.assertEqual(resultCode,201) # Created

      resultString, resultCode = user.put(u["username"], user_req)
      self.assertEqual(resultCode,204) # Updated

      result = user.get(u["username"])
      self.assertEqual(result, u) # get

      resultString, resultCode = user.get("nonExistantID")
      self.assertEqual(resultCode,404) 

      resultString, resultCode = user.delete(u["username"])
      self.assertEqual(resultCode,204) 
      resultString, resultCode = user.get("nonExistantID")
      self.assertEqual(resultCode,404) # deleted!

      resultString, resultCode = user.delete("nonExistantID")
      self.assertEqual(resultCode,404) 

      user.put(u["username"], user_req)
      user.put(u2["username"], user_req2)

      result = user.filter()
      self.assertIn( u, result )
      self.assertIn( u2, result )

      result = user.filter(roomNumber=u["roomNumber"])
      self.assertIn( u, result )
      self.assertNotIn( u2, result )

      result = user.filter(terms=u2["firstName"])
      self.assertNotIn( u, result )
      self.assertIn( u2, result )
 
      result = user.filter(terms=u2["firstName"], roomNumber=u["roomNumber"])
      self.assertIn( u, result )
      self.assertIn( u2, result )





unittest.main()
