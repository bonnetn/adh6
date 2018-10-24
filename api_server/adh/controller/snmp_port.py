from connexion import NoContent

from adh.auth import auth_regular_admin


@auth_regular_admin
def get_port_status(switchID, port_id):
    return NoContent, 200, True


@auth_regular_admin
def set_port_status(switchID, port_id, state):
    return NoContent, 200


@auth_regular_admin
def get_port_vlan(switchID, port_id):
    return NoContent, 200, 42


@auth_regular_admin
def set_port_vlan(switchID, port_id, vlan):
    return NoContent, 204

@auth_regular_admin
def get_port_mab(port_id):
    return False, 200

@auth_regular_admin
def set_port_mab(port_id, mab):
    return NoContent, 204
