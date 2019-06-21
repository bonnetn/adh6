from functools import lru_cache

import requests

from src.entity.configuration import Configuration


class OIDCServerGateway:
    def __init__(self, config: Configuration):
        self.config = config

    def get_tokens(self, authorization_code: str) -> dict:
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
            'code': authorization_code,
            'redirect_uri': self.config.REDIRECT_URI,
        }
        return requests.post(self.config.TOKEN_URL, verify=self.config.VERIFY_CERTS, data=params).json()

    @lru_cache()
    def oidc_jwk_cert(self) -> dict:
        resp = requests.get(
            self.config.JWK_URL,
            verify=self.config.VERIFY_CERTS,
            timeout=self.config.TIMEOUT
        )
        return resp.json()

