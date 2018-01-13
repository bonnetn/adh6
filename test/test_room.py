from controller import room
import unittest

d = { 
  'description'     : '7701',
  'roomNumber'      : 7701,
  'phone'           : 6842,
  'vlan'            : 49
}
d2 = { 
  'description'     : '7218',
  'roomNumber'      : 7218,
  'phone'           : 6843,
  'vlan'            : 48
}
class TestRoom(unittest.TestCase):

    def test(self):
      resultString, resultCode = room.putRoom(d["roomNumber"], d)
      print(resultString, resultCode)
      self.assertEqual(resultCode,201) # Created

      resultString, resultCode = room.putRoom(d["roomNumber"], d)
      self.assertEqual(resultCode,204) # Updated

      result = room.getRoom(d["roomNumber"])
      self.assertEqual(result, d) # getRoom

      resultString, resultCode = room.getRoom("nonExistantID")
      self.assertEqual(resultCode,404) 

      resultString, resultCode = room.deleteRoom(d["roomNumber"])
      self.assertEqual(resultCode,204) 
      resultString, resultCode = room.getRoom("nonExistantID")
      self.assertEqual(resultCode,404) # deleteRoomd!

      resultString, resultCode = room.deleteRoom("nonExistantID")
      self.assertEqual(resultCode,404) 

      room.putRoom(d["roomNumber"], d)
      room.putRoom(d2["roomNumber"], d2)

      result = room.filterRoom()
      self.assertIn( d, result )
      self.assertIn( d2, result )


