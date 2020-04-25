import functools
from flask import jsonify
from enum import Enum


class ResponseType(str, Enum):
    IN_CHANNEL = 'in_channel'
    EPHIMERAL = 'ephimeral'


class Response:
    def __init__(self, msg):
        self.msg = msg

    def as_json(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            return jsonify(res)
        return wrapper

    @as_json
    def as_public(self):
        return {
            'response_type': ResponseType.IN_CHANNEL,
            'text': self.msg
        }

    @as_json
    def as_ephimeral(self):
        return {
            'response_type': ResponseType.EPHIMERAL,
            'text': self.msg
        }
