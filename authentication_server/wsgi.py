from flask import Flask
from website.models import db, OAuth2Client
from website.oauth2 import config_oauth
from website.routes import bp
from CONFIGURATION import OAUTH2_CONF, FLASK_CONF


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config)
    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)
    with app.app_context():
        # Create tables in the DB
        db.create_all()

        # Create a base Client for ADH6 in the DB
        q = db.session.query(OAuth2Client)
        q = q.filter(OAuth2Client.client_id == OAUTH2_CONF["client_id"])
        if not q.one_or_none():
            cl = OAuth2Client(
                client_id=OAUTH2_CONF["client_id"],
                client_secret="",
                issued_at=1525600543,
                expires_at=0,
                redirect_uri=FLASK_CONF["adh6_url"],
                token_endpoint_auth_method="none",
                grant_type="implicit",
                response_type="token",
                scope="profile",
                client_name="adh6",
                logo_uri=FLASK_CONF["adh6_url"],
            )
            db.session.add(cl)
            db.session.commit()

    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')


application = create_app(FLASK_CONF)
