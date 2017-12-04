import port
import unittest
d = { 
  'portNumber'     : '1/0/4',
  'roomNumber'      : 5110,
  'switchID'       : 1
}
d2 = { 
  'portNumber'     : '1/0/5',
  'roomNumber'      : 7218,
  'switchID'       : 1
}

class TestPort(unittest.TestCase):

    def test(self):

      # POST
      resultString, resultCode, headers = port.createPort(1,d)
      self.assertEqual(resultCode,201) # Created
      portID = int(headers["Location"].split("/")[-1])

      # GET
      result = port.getPort( 1, portID )
      self.assertEqual(result, d) # getPort

      resultString, resultCode = port.getPort( 1, -42 )
      self.assertEqual(resultCode,404) 

      # DELETE
      resultString, resultCode = port.deletePort( 1, portID )
      self.assertEqual(resultCode,204) 
      resultString, resultCode = port.getPort( 1, portID )
      self.assertEqual(resultCode,404) # already deletePortd!

      resultString, resultCode = port.deletePort( 1,-42 )
      self.assertEqual(resultCode,404) 

      resultString, resultCode, headers = port.createPort(1, d)
      portID = int(headers["Location"].split("/")[-1])
      #UPDATE
      port.updatePort(1,portID, d2)
      result = port.getPort( 1, portID )
      self.assertEqual(result, d2) # 

      port.createPort(1, d)

      result = port.filterPort()
      self.assertIn( d, result )
      self.assertIn( d2, result )
     


unittest.main()
