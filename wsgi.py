#!/usr/bin/env python3
import connexion
import logging
from flask_cors import CORS
from adh.model.database import Database
from CONFIGURATION import PROD_DATABASE as DATABASE
from connexion.resolver import RestyResolver

Database.init_db(DATABASE)

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.app.config.update(
    AUTH_SERVER_ADDRESS='https://adh6.minet.net/oauth',
    APPLICATION_ROOT='/api',

)
app.add_api('swagger.yaml',
            resolver=RestyResolver('adh.controller'),
            strict_validation=True)
CORS(app.app)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    if Database.get_db():
        Database.get_db().remove_session()
