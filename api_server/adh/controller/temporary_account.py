import datetime
import logging
import secrets

from flask import g

from adh.auth import auth_super_admin
from adh.model.models import NainA
from adh.util.session_decorator import require_sql

TOKEN_SIZE = 32


@require_sql
@auth_super_admin
def create_temp_account(body):
    s = g.session
    firstname = body.get("firstname")
    lastname = body.get("lastname")
    if not firstname or not lastname:
        return "Empty first or last name", 400

    token = secrets.token_urlsafe(TOKEN_SIZE)
    naina = NainA(
        first_name=firstname,
        last_name=lastname,
        access_token=token,
        start_time=datetime.datetime.now(),
        expiration_time=datetime.datetime.now() + datetime.timedelta(hours=1),
        admin=g.admin.login,
    )
    s.add(naina)

    logging.info("%s created a temporary account for '%s %s'", g.admin.login, firstname, lastname)

    return {"accessToken": "NAINA_{}".format(token)}, 200
