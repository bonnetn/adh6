#!/usr/bin/env python3
import connexion
from connexion.resolver import RestyResolver

from config import CONFIGURATION
from config.CONFIGURATION import API_CONF, PROD_DATABASE
from src.interface_adapter.elasticsearch.storage import ElasticSearchStorage
from src.interface_adapter.sql.model.database import Database
from src.interface_adapter.sql.sql_storage import SQLStorage
from src.use_case.member_manager import MemberManager

Database.init_db(PROD_DATABASE)

sql_storage = SQLStorage()
elk_storage = ElasticSearchStorage(CONFIGURATION)
member_manager = MemberManager(
    member_storage=sql_storage,
    membership_storage=sql_storage,
    logs_storage=elk_storage,
    configuration=CONFIGURATION,

)

app = connexion.FlaskApp(__name__)
app.app.config.update(API_CONF)
app.add_api('swagger.yaml',
            resolver=RestyResolver('src.interface_adapter.http_api'),
            strict_validation=True)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
