# coding=utf-8
import json
import logging


class JSONFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        try:
            record.extra
        except AttributeError:
            return msg

        extra = json.dumps(record.extra)
        return f'{msg} | {extra}'


# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# add formatter to ch
ch.setFormatter(JSONFormatter('%(asctime)s [%(levelname)s]: %(message)s'))

# add ch to logger
logger.addHandler(ch)

LOG = logger
