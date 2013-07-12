# -*- coding: utf-8 -*-
from flask import Response
from functools import wraps
from flask import request, make_response, current_app
from .util import json_response
from .models import BearerToken, Consumer
from mongoengine.queryset import DoesNotExist
from base64 import b64decode
from .errors import token_error

from datetime import timedelta
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization', None)
        if authorization_header is not None:
            split_header = authorization_header.split(' ')
            if len(split_header) == 2 and split_header[0] == 'Bearer':
                encoded_token = split_header[1]
                try:
                    token = unicode(b64decode(encoded_token))
                except (TypeError, UnicodeDecodeError):
                    token_error('Incorrectly formatted token.')
                else:
                    try:
                        token = BearerToken.objects.get(token=token)
                    except DoesNotExist:
                        pass
                    else:
                        if not token.has_expired():
                            kwargs['bearer_token'] = token
                            return f(*args, **kwargs)
        return token_error()
    return decorated_function
