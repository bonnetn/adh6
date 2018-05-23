import requests
import requests.exceptions
from flask import current_app
from connexion import NoContent
from adh.model.database import Database as db
from adh.model.models import Utilisateur


def get_groups(token):
    try:
        headers = {"Authorization": "Bearer " + token}
        r = requests.get(
            current_app.config["AUTH_SERVER_ADDRESS"] + "/api/me",
            headers=headers,
            timeout=1
        )
    except requests.exceptions.ReadTimeout:
        return None

    if r.status_code != 200 or "uid" not in r.json():
        return None

    return r.json()


def token_info(access_token) -> dict:

    if current_app.config["TESTING"]:
        return {
            "uid": "TestingClient",
            "scope": ["profile"],
            "groups": []
        }

    infos = get_groups(access_token)
    if not infos:
        return None
    return {
        "uid": infos["uid"],
        "scope": ["profile"],
        "groups": infos["groups"]
    }


def auth_simple_user(f):
    def wrapper(*args, user, token_info, **kwargs):
        if current_app.config["TESTING"] \
           or "adh6_user" in token_info["groups"]:
            s = db.get_db().get_session()
            admin = Utilisateur.find(s, user)
            return f(admin, *args, **kwargs)
        return NoContent, 401
    return wrapper
