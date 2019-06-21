import json

import jwt

from src.entity.configuration import Configuration


class JWTController:
    def __init__(self, config: Configuration):
        self.config = config

    def parse(self, token: str, key: dict) -> dict:
        key_json = json.dumps(key['keys'][0])
        pubkey = jwt.algorithms.RSAAlgorithm.from_jwk(key_json)
        return jwt.decode(token, pubkey, algorithms='RS256', audience=self.config.CLIENT_ID)
