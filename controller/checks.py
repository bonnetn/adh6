from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, AddressValueError
import re

MAC_REGEX = re.compile('^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$')


def isMac(macAddress):
    """ Allowed MAC address format: DE:AD:BE:EF:01:23 """
    macAddress = str(macAddress).upper()
    return bool(MAC_REGEX.match(macAddress))

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


