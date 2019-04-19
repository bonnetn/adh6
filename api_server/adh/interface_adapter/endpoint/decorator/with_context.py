from functools import wraps

from flask import current_app

from adh.util.context import build_context


def with_context(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        ctx = build_context(testing=current_app.config["TESTING"])
        return f(ctx, *args, **kwds)

    return wrapper
