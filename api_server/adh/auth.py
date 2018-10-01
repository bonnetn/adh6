import os

import requests
import requests.exceptions
from connexion import NoContent
from flask import current_app

from adh.model.database import Database as db
from adh.model.models import Utilisateur


def get_groups(token):
    try:
        verify_cert = True
        if os.environ["ENVIRONMENT"] == "testing":
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
    if os.environ["ENVIRONMENT"] == "testing":
        result["groups"] = ["adh6_user", "adh6_admin"]  # If we are testing, consider the user as admin
    return result


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
        "uid": infos["id"],
        "scope": ["profile"],
        "groups": infos["groups"]
    }


def auth_regular_admin(f):
    def wrapper(*args, user, token_info, **kwargs):
        if current_app.config["TESTING"] \
                or "adh6_user" in token_info["groups"]:
            s = db.get_db().get_session()
            admin = Utilisateur.find_or_create(s, user)
            return f(admin, *args, **kwargs)
        return NoContent, 401

    return wrapper


def auth_super_admin(f):
    def wrapper(*args, user, token_info, **kwargs):
        if current_app.config["TESTING"] \
                or "adh6_admin" in token_info["groups"]:
            s = db.get_db().get_session()
            admin = Utilisateur.find_or_create(s, user)
            return f(admin, *args, **kwargs)
        return NoContent, 401

    return wrapper
