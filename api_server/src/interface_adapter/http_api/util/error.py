# coding=utf-8
def bad_request(err: ValueError):
    return f'Bad request: {repr(err)}.'
