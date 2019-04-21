# coding=utf-8
"""
With context decator.
"""
from functools import wraps

from flask import current_app

from src.util.context import build_context


def with_context(f):
    """
    Add context variable to the first argument of the http_api function.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """
        Wrap http_api function.
        """
        ctx = build_context(testing=current_app.config["TESTING"])
        return f(ctx, *args, **kwds)

    return wrapper
