# coding=utf-8
import string


def get_mac_variations(addr):
    addr = filter(lambda x: x in string.hexdigits, addr)
    addr = "".join(addr)
    addr = addr.lower()

    variations = []
    variations += ["{}:{}:{}:{}:{}:{}".format(*(addr[i * 2:i * 2 + 2] for i in range(6)))]
    variations += ["{}-{}-{}-{}-{}-{}".format(*(addr[i:i + 2] for i in range(6)))]
    variations += ["{}.{}.{}".format(*(addr[i:i + 4] for i in range(3)))]

    variations += list(map(lambda x: x.upper(), variations))

    return variations
