import logging
import os
import re
from typing import Set, Optional, Tuple

import requests

from src.controller.authz import AuthorizationController
from src.entity.api_definition import APIDefinition, EndpointDefinition
from src.entity.configuration import Configuration
from src.entity.request import Request
from src.handler.proxy import ProxyController


class ProxyControllerImpl(ProxyController):

    def __init__(self, config: Configuration, authz_controller: AuthorizationController,
                 api_definition: Set[APIDefinition]):
        self.config = config
        self.authz_controller = authz_controller
        self.api_definitions = api_definition

    def proxy(self, path: str, request: Request, tokens: dict) -> Tuple[str, int, dict]:
        # Discard unauthenticated users as soon as possible.
        if not _is_authenticated(tokens):
            return f'API Gateway: not authenticated', 401, {}

        # Check that this endpoint exists in the API/endpoint definition.
        api_def, endpoint_def = _get_defintions(self.api_definitions, path)
        if not endpoint_def or not api_def:
            return f'API Gateway: endpoint {path} is unknown', 404, {}

        policy = endpoint_def.authz  # Configured policy for this endpoint. Example: ADMIN_ONLY, DENY_ALL...
        allowed, reason = self.authz_controller.is_authorized(policy, tokens.get('id_token'))
        if not allowed:
            return f'API Gateway: you are not authorized to access the {path} endpoint: {reason}', 403, {}

        request_headers = dict(request.headers)
        del request_headers['Host']  # 'Host' will be set automatically.
        request_headers['Authorization'] = f'Bearer {_get_auth_token(tokens)}'  # Pass the JWT to downstream.

        logging.getLogger().info(
            f"proxy call {request.method} {api_def.host}/{path} (regex: {endpoint_def.path_regex})",
            extra={
                'method': request.method,
                'host': api_def.host,
                'path': path,
                'path_regex': endpoint_def.path_regex,
                'timeout': endpoint_def.timeout,
            })

        response = requests.request(
            method=request.method,
            url='/'.join([api_def.host, path]),
            params=dict(request.args),
            data=request.raw_content,
            headers=request_headers,
            timeout=endpoint_def.timeout,
            verify=api_def.cert,
        )

        def propagate(header: str):
            return _should_propagate_header(header, self.config.PROPAGATE_TO_CLIENT, endpoint_def)

        response_headers = dict((k, v) for k, v in response.headers.items() if propagate(k))

        return response.content, response.status_code, response_headers


def _get_defintions(config: Set[APIDefinition], path: str) -> \
        Tuple[Optional[APIDefinition], Optional[EndpointDefinition]]:
    # On normalize le path pour éviter tout probleme...
    # Exemple:
    #  api/member/../.././///admin/
    # Devient...
    #   admin/
    path = os.path.normpath(path)  # vire les "../" ou les "//" ou "/./".
    path = os.path.join(path, '')  # ajoute un '/' a la fin.

    for api in config:
        for endpoint in api.endpoints:
            if re.match(endpoint.path_regex, path):
                return api, endpoint

    return None, None


def _is_authenticated(tokens: dict) -> str:
    # TODO: renouveller les tokens si trop vieux.
    return tokens is not None and 'id_token' in tokens


def _get_auth_token(tokens: dict) -> str:
    return tokens['id_token']


def _should_propagate_header(header: str, headers_to_propagate: Set[str], definition: EndpointDefinition) -> bool:
    h = {h.casefold for h in headers_to_propagate} | {h.casefold() for h in definition.headers}
    if header.casefold() in h:
        return True

    return False
