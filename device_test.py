import device
import unittest
d = { 
  'macAddress'     : 'FF:FF:FF:FF:FF:FF',
  'ipAddress'      : '127.0.0.1',
  'ipv6Address'    : '12',
  'connectionType' : 'wired',
  'username'       : 'cazal_k'
}
d2 = { 
  'macAddress'     : '00:00:00:00:00:00',
  'ipAddress'      : '127.0.0.2',
  'ipv6Address'    : '13',
  'connectionType' : 'wireless',
  'username'       : 'bonnet_n'
}
class TestDevice(unittest.TestCase):

    def test(self):
      resultString, resultCode = device.putDevice(d["macAddress"], d)
      self.assertEqual(resultCode,201) # Created

      resultString, resultCode = device.putDevice(d["macAddress"], d)
      self.assertEqual(resultCode,204) # Updated

      result = device.getDevice( d["macAddress"] )
      self.assertEqual(result, d) # getDevice

      resultString, resultCode = device.getDevice( "nonExistantID" )
      self.assertEqual(resultCode,404) 

      resultString, resultCode = device.deleteDevice( d["macAddress"] )
      self.assertEqual(resultCode,204) 
      resultString, resultCode = device.getDevice( "nonExistantID" )
      self.assertEqual(resultCode,404) # deleteDeviced!

      resultString, resultCode = device.deleteDevice( "nonExistantID" )
      self.assertEqual(resultCode,404) 

      device.putDevice(d["macAddress"], d)
      device.putDevice(d2["macAddress"], d2)

      result = device.filterDevice()
      self.assertIn( d, result )
      self.assertIn( d2, result )

      result = device.filterDevice(username='cazal_k')
      self.assertIn( d, result )
      self.assertNotIn( d2, result )

     


unittest.main()
