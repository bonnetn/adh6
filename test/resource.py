base_url = ""
device_cazal = {
    'mac': 'FF:FF:FF:FF:FF:FF',
    'ipAddress': '127.0.0.1',
    'ipv6Address': '12',
    'connectionType': 'wired',
    'username': 'cazal_k'
}

device_bonnet = {
    'mac': '00:00:00:00:00:00',
    'ipAddress': '127.0.0.2',
    'ipv6Address': '13',
    'connectionType': 'wireless',
    'username': 'bonnet_n'
}

INVALID_IP = [
    "",                  # Empty string
    "randomString",      # Some random data
    "192.168",           # Unfinished string
    "....",              # Only delimiters
    "200.256.200.200",   # Number > 255
    "-1.200.200.200",    # Number < 0
    "192.168.0.0/24",    # Address with mask
    "192.168.0.0-10",    # Address range
    42,                  # Wrong type
]

INVALID_MAC = [
    "",                      # Empty string
    "AA:AA:AA:",             # Unfinished MAC address
    "AA:AA:AA:AA:AA:AA:BB",  # MAC address too long
    "randomString",          # Random data
    ":::::",                 # Only delimiters
    "12:34:56:78:9A:BG",     # Non hexa byte (BG)
    42,                      # Wrong type
]
