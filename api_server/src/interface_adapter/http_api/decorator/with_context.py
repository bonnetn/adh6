# coding=utf-8
"""
With context decator.
"""
import uuid
from flask import current_app
from functools import wraps

from src.util.context import build_context


def with_context(f):
    """
    Add context variable to the first argument of the http_api function.
    """

    @wraps(f)
    def wrapper(cls, *args, **kwds):
        """
        Wrap http_api function.
        """
        ctx = build_context(
            testing=current_app.config["TESTING"],
            request_id=str(uuid.uuid4()),  # Generates an unique ID on this request so we can track it.
        )
        return f(cls, ctx, *args, **kwds)

    return wrapper
