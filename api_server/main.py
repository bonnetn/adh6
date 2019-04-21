#!/usr/bin/env python3
import connexion
import logging
from connexion.resolver import RestyResolver

from adh.config import CONFIGURATION
from adh.config.CONFIGURATION import API_CONF
from adh.config.CONFIGURATION import PROD_DATABASE as DATABASE
from adh.interface_adapter.elasticsearch.storage import ElasticSearchStorage
from adh.interface_adapter.sql.model.database import Database
from adh.interface_adapter.sql.sql_storage import SQLStorage
from adh.use_case.member_manager import MemberManager

Database.init_db(DATABASE)

sql_storage = SQLStorage()
elk_storage = ElasticSearchStorage()
member_manager = MemberManager(
    member_storage=sql_storage,
    membership_storage=sql_storage,
    logs_storage=elk_storage,
    configuration=CONFIGURATION,

)

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.app.config.update(API_CONF)
app.add_api('swagger.yaml',
            resolver=RestyResolver('adh.interface_adapter.endpoint'),
            strict_validation=True)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
