import ipaddress


class NoMoreIPAvailable(Exception):
    pass


def get_available_ip(network, ip_taken):
    network = ipaddress.ip_network(network)
    ip_taken = set(map(lambda x: ipaddress.ip_address(x), ip_taken))
    available = filter(lambda x: x not in ip_taken, network.hosts())
    try:
        ip = next(available)
    except StopIteration:
        raise NoMoreIPAvailable

    return str(ip)
