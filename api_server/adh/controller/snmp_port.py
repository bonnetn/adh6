from connexion import NoContent
from adh.auth import auth_simple_user


@auth_simple_user
def get_port_status(switchID, port_id):
    return 204, NoContent, True


@auth_simple_user
def set_port_status(switchID, port_id, state):
    return 200, NoContent


@auth_simple_user
def get_port_vlan(switchID, port_id):
    return 200, NoContent, 42


@auth_simple_user
def set_port_vlan(switchID, port_id, vlan):
    return 204, NoContent
