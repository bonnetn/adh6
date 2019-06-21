import logging
from datetime import timedelta

from flask import Flask
from flask_session import Session

from src.controller.authn import AuthenticationControllerImpl
from src.controller.authz import AuthorizationController
from src.controller.jwt_parser import JWTController
from src.controller.proxy import ProxyControllerImpl
from src.endpoints import ENDPOINTS
from src.entity.configuration import Configuration
from src.gateway.ldap import LDAPGateway
from src.gateway.oidc_server import OIDCServerGateway
from src.handler.authn import AuthNHandler
from src.handler.proxy import ProxyHandler


def create_app():
    #############################
    # CREATION DE L'APPLICATION #
    #############################
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    ####################################
    # CONFIGURATION DES SESSIONS FLASK #
    ####################################
    # Un peu moins qu'un jour pour qu'on doive se re-log tous les jours.
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=20)

    # On stocke sur un volume partagé entre toutes les instances, c'est pas le mieux mais c'est ce qu'il y a de plus simple.
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/sessions'
    Session(app)

    #############################
    # INJECTION DES DEPENDANCES #
    #############################
    config = Configuration()
    oidc_server_gateway = OIDCServerGateway(config)
    ldap_gateway = LDAPGateway(config)

    jwt_parser = JWTController(config)
    authz_controller = AuthorizationController(config, oidc_server_gateway, jwt_parser, ldap_gateway)
    authn_controller = AuthenticationControllerImpl(config, oidc_server_gateway)
    proxy_controller = ProxyControllerImpl(config, authz_controller, ENDPOINTS)

    auth_handler = AuthNHandler(authn_controller)
    proxy_handler = ProxyHandler(proxy_controller)

    ###############################
    # AJOUT DES ENDPOINTS A FLASK #
    ###############################
    app.register_blueprint(auth_handler.blueprint)
    app.register_blueprint(proxy_handler.blueprint)

    return app
