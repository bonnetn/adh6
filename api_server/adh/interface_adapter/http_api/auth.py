import datetime

import requests
import requests.exceptions
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound

from adh.interface_adapter.sql.model.database import Database as Db
from adh.interface_adapter.sql.model.models import NainA
from adh.util.env import isDevelopmentEnvironment

ADH6_USER = "adh6_user"
ADH6_ADMIN = "adh6_admin"


def token_info(access_token) -> dict:
    if access_token.startswith("NAINA_"):
        return authenticate_temp_account(access_token[6:])

    if current_app.config["TESTING"]:
        return {
            "uid": "TestingClient",
            "scope": ["profile"],
            "groups": []
        }
    return authenticate_against_sso(access_token)


def authenticate_temp_account(access_token):
    s = Db.get_db().get_session()

    q = s.query(NainA)
    q = q.filter(NainA.access_token == access_token)
    try:
        naina = q.one()
        now = datetime.datetime.now()
        if naina.expiration_time > now > naina.start_time:  # Make sure the token is still valid.
            return {
                "uid": "TEMP_ACCOUNT({})[{} {}]".format(naina.id, naina.first_name, naina.last_name),
                "scope": ["profile"],
                "groups": [ADH6_USER]
            }
        else:
            return None  # Expired token.
    except NoResultFound:
        return None  # No token found.
    finally:
        s.close()


def get_sso_groups(token):
    try:
        verify_cert = True
        if isDevelopmentEnvironment():
            verify_cert = False

        headers = {"Authorization": "Bearer " + token}
        r = requests.get(
            current_app.config["AUTH_SERVER_ADDRESS"],
            headers=headers,
            timeout=1,
            verify=verify_cert
        )
    except requests.exceptions.ReadTimeout:
        return None

    if r.status_code != 200 or "id" not in r.json():
        return None

    result = r.json()
    if isDevelopmentEnvironment():
        result["groups"] = [ADH6_USER, ADH6_ADMIN]  # If we are testing, consider the user asg.admin
    return result


def authenticate_against_sso(access_token):
    infos = get_sso_groups(access_token)
    if not infos:
        return None
    return {
        "uid": infos["id"],
        "scope": ["profile"],
        "groups": infos["groups"]
    }
