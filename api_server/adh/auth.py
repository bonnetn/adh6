import os

import requests
import requests.exceptions
from connexion import NoContent
from flask import current_app, g

from adh.model.models import Utilisateur
from adh.util.env import isDevelopmentEnvironment

ADH6_USER = "adh6_user"
ADH6_ADMIN = "adh6_admin"


def get_groups(token):
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


def token_info(access_token) -> dict:
    if current_app.config["TESTING"]:
        return {
            "uid": "TestingClient",
            "scope": ["profile"],
            "groups": []
        }

    if access_token.startswith("NAINA_"):
        return {
            "uid": "nain_a",
            "scope": ["profile"],
            "groups": [ADH6_USER]
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
                or ADH6_USER in token_info["groups"]:
            g.admin = Utilisateur.find_or_create(g.session, user)
            return f(*args, **kwargs)
        return NoContent, 401

    return wrapper


def auth_super_admin(f):
    def wrapper(*args, user, token_info, **kwargs):
        if current_app.config["TESTING"] \
                or ADH6_ADMIN in token_info["groups"]:
            g.admin = Utilisateur.find_or_create(g.session, user)
            return f(*args, **kwargs)
        return NoContent, 401

    return wrapper
