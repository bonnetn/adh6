import datetime
import ipaddress

from adh.model.models import Ordinateur, Adherent


class NoMoreIPAvailable(Exception):
    pass


def get_available_ip(network, ip_taken):
    network = ipaddress.ip_network(network)
    ip_taken = set(map(lambda x: ipaddress.ip_address(x), ip_taken))
    available = filter(lambda x: x not in ip_taken, network.hosts())
    try:
        # two times "next()" because we want to skip the first address, which
        # is the gateway address
        next(available)
        ip = next(available)
    except StopIteration:
        raise NoMoreIPAvailable

    return str(ip)


def get_all_used_ipv4(session):
    q = session.query(Ordinateur)
    q = q.filter(Ordinateur.ip != "En Attente")
    return list(map(lambda x: x.ip, q.all()))


def get_all_used_ipv6(session):
    q = session.query(Ordinateur)
    q = q.filter(Ordinateur.ipv6 != "En Attente")
    return list(map(lambda x: x.ipv6, q.all()))


def get_expired_devices(session):
    q = session.query(Ordinateur)
    q = q.filter(Ordinateur.ip != "En Attente")
    q = q.join(Adherent)
    q = q.filter(Adherent.date_de_depart < datetime.datetime.now())
    return list(q.all())


def free_expired_devices(session):
    for dev in get_expired_devices(session):
        dev.ip = "En Attente"
        dev.ipv6 = "En Attente"
