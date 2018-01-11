from string import hexdigits
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, AddressValueError

def isMac ( macAddress ):
    """ Allowed MAC address format: DE:AD:BE:EF:01:23 """
    splittedMac = macAddress.split(':')
    if len(splittedMac) != 6:
        return False
    for byte in splittedMac:
        if len(byte) != 2:
            return False
    for c in macAddress:
        if c not in hexdigits+':':
            return False
    return True

def checkDate( dateString ):
    """ Allowed date format: YYYY-MM-DD """
    splittedDate = dateString.split('-')
    if len(splittedDate) != 3  or len(splittedDate[0]) != 4\
    or len(splittedDate[1]) != 2 or len(splittedDate[2]) != 2:
        return False
    else:
        try:
            datetime(int(splittedDate[0]), int(splittedDate[1]), int(splittedDate[2]))
        except (TypeError, ValueError):
            return False
    return True 

def isIPv4 ( ipAddress ):
    """ Allowed format: 192.168.0.1 """
    try:
        IPv4Address(ipAddress)
    except AddressValueError:
        return False
    return True

def isIPv6 ( ipAddress ):
    """ Allowed format: fe80:0000:0000:0000:62eb:69ff:feec:c643 """
    try:
        IPv6Address(ipAddress)
    except AddressValueError:
        return False
    return True


