from abc import ABC, abstractmethod
from typing import Optional, Tuple

from flask import request, session, Blueprint, redirect

from src.handler.constant import SESSION_TOKEN, SESSION_STATE


class AuthenticationController(ABC):
    @abstractmethod
    def login(self) -> Tuple[str, str]:
        """

        :return: (redirect URL, 'state' token to be stored on the session)
        """
        pass

    @abstractmethod
    def get_tokens(self, state: str, authorization_code: str, stored_state: str) -> \
            Tuple[Optional[dict], Optional[str]]:
        """
        Return the token information (access token, JWT...) from the authorization_code.
        Can return an error message.

        :param state: received state
        :param authorization_code: receive code
        :param stored_state: state from session
        :return: (token information, error msg)
        """
        pass


class AuthNHandler:
    def __init__(self, controller: AuthenticationController):
        self.blueprint = Blueprint('auth_blueprint', __name__)

        @self.blueprint.route('/api/login')
        def step1_login():
            """
            STEP 1: User navigates to /login. Redirect them to the authentication backend (CAS).
            """
            redirect_url, state = controller.login()
            session[SESSION_STATE] = state
            return redirect(redirect_url)

        @self.blueprint.route('/api/authorization-code')
        def step2_authorization_code():
            """
            STEP 2: User went to the authentication backend, entered their credential and then got
            redirected back to this endpoint with some data in args.

            We now have a temporary 'authorization_token' that we can use to fetch a permanent 'access_token'.
            In order to get this new token, we must call the the auth backend (CAS).
            """
            args = request.args
            token, err = controller.get_tokens(
                state=args.get('state'),
                authorization_code=args.get('code'),
                stored_state=session.get(SESSION_STATE),
            )
            if token is None:
                return err, 400

            del session[SESSION_STATE]  # Prevent state reuse.
            session[SESSION_TOKEN] = token

            return str(token)
