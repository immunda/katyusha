# -*- coding: utf-8 -*-
from flask import Response
from functools import wraps
from flask import request
from codeclubworld.api.models import BearerToken, Consumer
from mongoengine.queryset import DoesNotExist
from base64 import b64decode


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization', None)
        if authorization_header is not None:
            split_header = authorization_header.split(' ')
            if len(split_header) == 2 and split_header[0] == 'Bearer':
                encoded_token = split_header[1]
                try:
                    token = b64decode(encoded_token)
                except TypeError:
                    pass
                else:
                    try:
                        BearerToken.objects.get(token=token)
                    except DoesNotExist:
                        pass
                    else:
                        return f(*args, **kwargs)
        return Response(status=401)
    return decorated_function
