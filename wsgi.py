from flask import Flask
from website.models import db, OAuth2Client
from website.oauth2 import config_oauth
from website.routes import bp


ADH6_IMPLICIT_ID = "H4XcptJlYAWAqyxTJxybMXfi"


def create_app(config=None):
    app = Flask(__name__)
    #
    # # load default configuration
    # app.config.from_object('website.settings')
    #
    # # load environment configuration
    # if 'WEBSITE_CONF' in os.environ:
    #     app.config.from_envvar('WEBSITE_CONF')
    #
    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        q = db.session.query(OAuth2Client)
        q = q.filter(OAuth2Client.client_id == ADH6_IMPLICIT_ID)
        if not q.one_or_none():
            cl = OAuth2Client(
                client_id=ADH6_IMPLICIT_ID,
                client_secret="",
                issued_at=1525600543,
                expires_at=0,
                redirect_uri="https://adh6.minet.net",
                token_endpoint_auth_method="none",
                grant_type="implicit",
                response_type="token",
                scope="profile",
                client_name="adh6",
                logo_uri="https://adh6.minet.net",
            )
            db.session.add(cl)
            db.session.commit()

    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')


application = create_app({
    'APPLICATION_ROOT': '/oauth',
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
    'ADH6_ADDRESS': 'https://adh6.minet.net',
})
