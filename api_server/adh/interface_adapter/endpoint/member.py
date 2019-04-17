import datetime
import hashlib
import json
import logging
import string

from connexion import NoContent
from elasticsearch5 import Elasticsearch
from flask import current_app, g

from CONFIGURATION import ELK_HOSTS
from CONFIGURATION import PRICES
from adh.exceptions import InvalidEmail, RoomNotFound, MemberNotFound
from adh.interface_adapter.endpoint.auth import auth_regular_admin
from adh.interface_adapter.endpoint.decorator.session_decorator import require_sql
from adh.interface_adapter.endpoint.device_utils import get_all_devices
from adh.interface_adapter.sql.model.models import Adherent, Chambre, Adhesion, Modification
from adh.util.context import build_context
from adh.util.date import string_to_date
from main import member_manager


def adherent_exists(s, username):
    """ Returns true if the member exists """
    try:
        Adherent.find(s, username)
    except MemberNotFound:
        return False
    return True


@require_sql
@auth_regular_admin
def search(limit=100, offset=0, terms=None, roomNumber=None):
    """ [API] Filter the list of members from the the database """
    ctx = build_context(
        session=g.session,
        admin=g.admin,
    )
    try:
        result, total_count = member_manager.search(ctx, limit, offset, roomNumber, terms)
        headers = {
            "X-Total-Count": str(total_count),
            'access-control-expose-headers': 'X-Total-Count'
        }
        return result, 200, headers
    except ValueError as e:
        return f'Wrong argument: {e}.', 400


@require_sql
@auth_regular_admin
def get(username):
    """ [API] Get the specified member from the database """
    ctx = build_context(
        session=g.session,
        admin=g.admin,
    )
    try:
        return member_manager.get_by_username(ctx, username), 200
    except MemberNotFound:
        return NoContent, 404


@require_sql
@auth_regular_admin
def delete(username):
    """ [API] Delete the specified User from the database """
    s = g.session

    # Find the soon-to-be deleted user
    try:
        a = Adherent.find(s, username)
    except MemberNotFound:
        return NoContent, 404

    try:
        # if so, start tracking for modifications
        a.start_modif_tracking()

        # Actually delete it
        s.delete(a)

        # Write it in the modification table
        Modification.add(s, a, g.admin)
    except Exception:
        raise
    logging.info("%s deleted the member %s", g.admin.login, username)
    return NoContent, 204


@require_sql
@auth_regular_admin
def patch(username, body):
    """ [API] Partially update a member from the database """
    s = g.session

    # Create a valid object

    # Check if it already exists
    update = adherent_exists(s, username)

    if not update:
        return NoContent, 404

    member = Adherent.find(s, username)
    member.start_modif_tracking()
    try:
        member.nom = body.get("lastName", member.nom)
        member.prenom = body.get("firstName", member.prenom)
        member.mail = body.get("email", member.mail)
        member.commentaires = body.get("comment", member.commentaires)
        member.login = body.get("username", member.login)
        if "departureDate" in body:
            member.date_de_depart = string_to_date(body["departureDate"])
        if "associationMode" in body:
            member.mode_association = string_to_date(body["associationMode"])
        if "roomNumber" in body:
            member.chambre = Chambre.find(s, body["roomNumber"])
    except InvalidEmail:
        return "Invalid email", 400
    except RoomNotFound:
        return "No room found", 400
    except ValueError:
        return "String must not be empty", 400

    # Create the corresponding modification
    Modification.add(s, member, g.admin)

    logging.info("%s updated the member %s\n%s",
                 g.admin.login, username, json.dumps(body, sort_keys=True))
    return NoContent, 204


@require_sql
@auth_regular_admin
def put(username, body):
    """ [API] Create/Update member from the database """
    s = g.session

    # Create a valid object
    try:
        new_member = Adherent.from_dict(s, body)
    except InvalidEmail:
        return "Invalid email", 400
    except RoomNotFound:
        return "No room found", 400
    except ValueError:
        return "String must not be empty", 400

    # Check if it already exists
    update = adherent_exists(s, username)

    if update:
        current_adh = Adherent.find(s, username)
        new_member.id = current_adh.id
        current_adh.start_modif_tracking()

    # Merge the object (will create a new if it doesn't exist)
    new_member = s.merge(new_member)

    # Create the corresponding modification
    Modification.add(s, new_member, g.admin)

    if update:
        logging.info("%s updated the member %s\n%s",
                     g.admin.login, username, json.dumps(body, sort_keys=True))
        return NoContent, 204
    else:
        logging.info("%s created the member %s\n%s",
                     g.admin.login, username, json.dumps(body, sort_keys=True))
        return NoContent, 201


@require_sql
@auth_regular_admin
def post_membership(username, body):
    """ [API] Add a membership record in the database """
    s = g.session

    start = datetime.datetime.now().date()
    if "start" in body:
        start = string_to_date(body["start"])

    duration = body["duration"]
    end = start + datetime.timedelta(days=duration)

    if duration not in PRICES:
        return "There is no price assigned to that duration", 400

    try:
        adh = Adherent.find(s, username)
        s.add(Adhesion(
            adherent=adh,
            depart=start,
            fin=end
        ))
        adh.start_modif_tracking()
        adh.date_de_depart = end

    except MemberNotFound:
        return NoContent, 404

    Modification.add(s, adh, g.admin)
    logging.info("%s created the membership record %s\n%s",
                 g.admin.login, username, json.dumps(body, sort_keys=True))
    return NoContent, 200, {'Location': 'test'}  # TODO: finish that!


def ntlm_hash(txt):
    """
    NTLM hashing function
    wow much security such hashing function
    Needed by MSCHAPv2.
    """

    return hashlib.new('md4', txt.encode('utf-16le')).hexdigest()


@require_sql
@auth_regular_admin
def put_password(username, body):
    password = body["password"]
    s = g.session

    try:
        a = Adherent.find(s, username)
    except MemberNotFound:
        return NoContent, 404

    a.start_modif_tracking()
    a.password = ntlm_hash(password)

    # Build the corresponding modification
    Modification.add(s, a, g.admin)

    logging.info("%s updated the password of %s",
                 g.admin.login, username)
    return NoContent, 204


def _get_mac_variations(addr):
    addr = filter(lambda x: x in string.hexdigits, addr)
    addr = "".join(addr)
    addr = addr.lower()

    variations = []
    variations += ["{}:{}:{}:{}:{}:{}".format(*(addr[i * 2:i * 2 + 2] for i in range(6)))]
    variations += ["{}-{}-{}-{}-{}-{}".format(*(addr[i:i + 2] for i in range(6)))]
    variations += ["{}.{}.{}".format(*(addr[i:i + 4] for i in range(3)))]

    variations += list(map(lambda x: x.upper(), variations))

    return variations


@require_sql
@auth_regular_admin
def get_logs(username):
    s = g.session

    if not ELK_HOSTS:
        logging.warn("No elasticsearch node configured. Returning empty response.")
        return NoContent, 200

    # If the member does not exist, return 404
    try:
        Adherent.find(s, username)
    except MemberNotFound:
        return NoContent, 404

    # Prepare the elasticsearch query...
    query = {
        "sort": {
            '@timestamp': 'desc',  # Sort by time
        },
        "query": {
            "bool": {
                "should": [  # "should" in a "bool" query basically act as a "OR"
                    {"match": {"message": username}},  # Match every log mentioning this member
                    # rules to match MACs addresses are added in the next chunk of code
                ],
                "minimum_should_match": 1,
            },
        },
        "_source": ["@timestamp", "message"],  # discard any other field than timestamp & message
        "size": 100,  # TODO(insolentbacon): make a parameter in the request to change this value
    }

    # Fetch all the devices of the member to put them in the request
    all_devices = get_all_devices(s)
    q = s.query(all_devices, Adherent.login.label("login"))
    q = q.join(Adherent, Adherent.id == all_devices.columns.adherent_id)
    q = q.filter(Adherent.login == username)
    mac_tbl = list(map(lambda x: x.mac, q.all()))

    # Add the macs to the "should"
    for addr in mac_tbl:
        variations = map(
            lambda x: {"match_phrase": {"message": x}},
            _get_mac_variations(addr)
        )
        query["query"]["bool"]["should"] += list(variations)

    logging.info("%s fetched the logs of %s", g.admin.login, username)
    if current_app.config["TESTING"]:  # Do not actually query elasticsearch if testing...
        return ["test_log"], 200

    # TODO(insolentbacon): instantiate only once the Elasticsearch client
    es = Elasticsearch(ELK_HOSTS)
    res = es.search(index="", body=query)['hits']['hits']

    return list(map(
        lambda x: "{} {}".format(x["_source"]["@timestamp"], x["_source"]["message"]),
        res
    )), 200
