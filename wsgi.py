import os
from flask import Flask
from website.models import db
from website.oauth2 import config_oauth
from website.routes import bp


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
    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')

application = create_app({
    'APPLICATION_ROOT': '/oauth',
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
    'ADH6_ADDRESS': 'https://adh6.minet.net',
})
