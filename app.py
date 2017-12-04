#!/usr/bin/env python3
import connexion
import datetime
import logging
from flask_cors import CORS

from connexion import NoContent

logging.basicConfig(level=logging.INFO)
#app = connexion.App(__name__)
app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml')
CORS(app.app)
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=3000, server='gevent')


