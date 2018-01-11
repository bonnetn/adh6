from controller import switch
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
      resultString, resultCode, headers = switch.createSwitch(d)
      self.assertEqual(resultCode,201) # Created
      switchID = int(headers["Location"].split("/")[-1])

      # GET
      result = switch.getSwitch(switchID)
      self.assertEqual(result, d) # getSwitch

      resultString, resultCode = switch.getSwitch(-42)
      self.assertEqual(resultCode,404) 

      # DELETE
      resultString, resultCode = switch.deleteSwitch(switchID)
      self.assertEqual(resultCode,204) 
      resultString, resultCode = switch.getSwitch(switchID)
      self.assertEqual(resultCode,404) # already deleteSwitchd!

      resultString, resultCode = switch.deleteSwitch(-42)
      self.assertEqual(resultCode,404) 

      resultString, resultCode, headers = switch.createSwitch(d)
      switchID = int(headers["Location"].split("/")[-1])
      switchIDd2 = switchID

      #UPDATE
      switch.updateSwitch(switchID, d2)
      result = switch.getSwitch(switchID)
      self.assertEqual(result, d2) # 

      resultString, resultCode, headers = switch.createSwitch(d)
      switchIDd = int(headers["Location"].split("/")[-1])

      result = switch.filterSwitch()
      self.assertIn( {'switchID':switchIDd, 'switch':d}, result )
      self.assertIn( {'switchID':switchIDd2, 'switch':d2}, result )
     


unittest.main()
