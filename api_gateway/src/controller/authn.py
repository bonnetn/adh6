import uuid
from typing import Optional, Tuple
from urllib.parse import urlencode

from src.entity.configuration import Configuration
from src.gateway.oidc_server import OIDCServerGateway
from src.handler.authn import AuthenticationController


class AuthenticationControllerImpl(AuthenticationController):
    def __init__(self, config: Configuration, gateway: OIDCServerGateway):
        self.gateway = gateway
        self.config = config

    def login(self) -> (str, str):
        state = _generate_state_token()
        params = {
            'response_type': 'code',
            'client_id': self.config.CLIENT_ID,
            'redirect_uri': self.config.REDIRECT_URI,
            'state': state,
            'scope': 'openid',
        }
        return f'{self.config.AUTHORIZE_URL}?{urlencode(params)}', state

    def get_tokens(self, state: str, authorization_code: str, stored_state: str) -> \
            Tuple[Optional[dict], Optional[str]]:
        if stored_state is None:
            return None, "API Gateway: query parameter 'state' is required"

        if state != stored_state:
            return None, "API Gateway: query parameter 'state' is invalid"

        return self.gateway.get_tokens(authorization_code), None


def _generate_state_token() -> str:
    return str(uuid.uuid4())
