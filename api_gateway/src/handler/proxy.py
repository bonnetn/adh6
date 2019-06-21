from abc import ABC, abstractmethod
from typing import Tuple

from flask import request, Blueprint, session

from src.entity.request import Request
from src.handler.constant import SESSION_TOKEN


class ProxyController(ABC):
    @abstractmethod
    def proxy(self, path: str, request: Request, tokens: dict) -> Tuple[str, int, dict]:
        """
        :param path:
        :param request:
        :return: (content, status code, headers)
        """
        pass


class ProxyHandler:
    def __init__(self, controller: ProxyController):
        self.blueprint = Blueprint('proxy_blueprint', __name__)

        @self.blueprint.route('/', defaults={'path': ''})
        @self.blueprint.route('/<path:path>', methods=['GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'])
        def proxy(path):
            return controller.proxy(
                path,
                Request(
                    method=request.method,
                    args=request.args,
                    headers=request.headers,
                    raw_content=request.stream.read(),
                ),
                session.get(SESSION_TOKEN)
            )
