# coding=utf-8
"""
With context decator.
"""
from functools import wraps

from flask import current_app

from adh.util.context import build_context


def with_context(f):
    """
    Add context variable to the first argument of the endpoint function.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """
        Wrap endpoint function.
        """
        ctx = build_context(testing=current_app.config["TESTING"])
        return f(ctx, *args, **kwds)

    return wrapper
