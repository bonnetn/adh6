from connexion import NoContent
from adh.auth import auth_regular_admin


@auth_regular_admin
def get_port_status(switchID, port_id):
    return 204, NoContent, True


@auth_regular_admin
def set_port_status(switchID, port_id, state):
    return 200, NoContent


@auth_regular_admin
def get_port_vlan(switchID, port_id):
    return 200, NoContent, 42


@auth_regular_admin
def set_port_vlan(switchID, port_id, vlan):
    return 204, NoContent
