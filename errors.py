# -*- coding: utf-8 -*-
from .util import json_response


def token_error(message=None):
    if message is None:
        message = 'Invalid or expired token.'

    data = {
        'errors': [{
            'message': message,
        }]
    }
    return json_response(data, status=401)
