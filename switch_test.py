import switch
import unittest
d = { 
  'description'     : 'Switch',
  'ip'              : "192.168.0.1",
  'community'       : "test"
}
d2 = { 
  'description'     : 'Switch2',
  'ip'              : "192.168.0.2",
  'community'       : "tototo"
}



class TestSwitch(unittest.TestCase):

    def test(self):

      # POST
      resultString, resultCode, headers = switch.create(d)
      self.assertEqual(resultCode,201) # Created
      switchID = int(headers["Location"].split("/")[-1])

      # GET
      result = switch.get( switchID )
      self.assertEqual(result, d) # get

      resultString, resultCode = switch.get( -42 )
      self.assertEqual(resultCode,404) 

      # DELETE
      resultString, resultCode = switch.delete( switchID )
      self.assertEqual(resultCode,204) 
      resultString, resultCode = switch.get(switchID )
      self.assertEqual(resultCode,404) # already deleted!

      resultString, resultCode = switch.delete( -42 )
      self.assertEqual(resultCode,404) 

      resultString, resultCode, headers = switch.create(d)
      switchID = int(headers["Location"].split("/")[-1])

      #UPDATE
      switch.update(switchID, d2)
      result = switch.get( switchID )
      self.assertEqual(result, d2) # 

      switch.create(d)

      result = switch.filter()
      self.assertIn( d, result )
      self.assertIn( d2, result )
     


unittest.main()
