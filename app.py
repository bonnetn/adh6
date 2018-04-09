#!/usr/bin/env python3
import connexion
import logging
from flask_cors import CORS
from model.database import Database
from settings.settings import DATABASE
from connexion.resolver import RestyResolver


logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml', resolver=RestyResolver('adh'))
CORS(app.app)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    if Database.get_db():
        Database.get_db().remove_session()


if __name__ == '__main__':
    Database.init_db(DATABASE)
    # run our standalone gevent server
    app.run(port=3000, server='gevent')
