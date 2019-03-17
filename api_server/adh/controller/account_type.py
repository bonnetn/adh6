import datetime
import json
import logging
import requests

import dateutil
from connexion import NoContent
from flask import g
from sqlalchemy.orm.exc import MultipleResultsFound

from adh.auth import auth_regular_admin
from adh.model import models
from adh.util.session_decorator import require_sql

@require_sql
@auth_regular_admin
def filter_account_type(limit=100, offset=0, terms=None):
    pass

@require_sql
@auth_regular_admin
def create_account_type(body):
    pass

@require_sql
@auth_regular_admin
def get_account_type(account_type_id):
    pass

@require_sql
@auth_regular_admin
def patch_account_type(account_type_id, body):
    pass

