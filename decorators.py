# -*- coding: utf-8 -*-
from flask import Response
from functools import wraps

from flask import request


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # denied
        print request.headers
        if True:
            return Response(status=401)
        return f(*args, **kwargs)
    return decorated_function
