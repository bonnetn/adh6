from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from .models import db
from .models import OAuth2Client, OAuth2Token
import authlib.specs.oidc.grants

authorization = AuthorizationServer()
require_oauth = ResourceProtector()


def config_oauth(app):
    query_client = create_query_client_func(db.session, OAuth2Client)
    save_token = create_save_token_func(db.session, OAuth2Token)
    authorization.init_app(
        app, query_client=query_client, save_token=save_token)

    # support implicit grant
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(authlib.specs.oidc.grants.OpenIDImplicitGrant)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())
