import ipaddress
import datetime
from adh.model.models import Ordinateur, Adherent


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


def get_all_used_ip(session):
    q = session.query(Ordinateur)
    q = q.filter(Ordinateur.ip != "En Attente")
    return list(map(lambda x: x.ip, q.all()))


def get_expired_devices(session):
    q = session.query(Ordinateur)
    q = q.filter(Ordinateur.ip != "En Attente")
    q = q.join(Adherent)
    q = q.filter(Adherent.date_de_depart < datetime.datetime.now())
    for i in q.all():
        print(i.adherent.date_de_depart < datetime.datetime.now())
    return list(q.all())
