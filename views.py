# -*- coding: utf-8 -*-
from flask.views import MethodView, request
from flask import Response
from .util import json_response
from .models import *
from mongoengine.queryset import DoesNotExist
from .decorators import crossdomain


class ApiView(MethodView):

    def safe_int(self, get_dict, key, fallback, maximum=None):
        try:
            value = int(get_dict.get(key, fallback))
        except ValueError:
            value = fallback
        if maximum is not None and value > maximum:
            value = maximum
        return value

    # Successful
    def created(self):
        return Response(status=201)

    # Client error
    def bad_request(self):
        return Response(status=400)

    def unauthorized(self):
        return Response(status=401)

    def not_found(self):
        return Response(status=404)

    def not_acceptable(self):
        return Response(status=406)

    def unsupported_media_type(self):
        return Response(status=415)

    @crossdomain(origin='*', headers=['*'])
    def options(self, **kwargs):
        return super(ApiView, self).options()


class TokenView(ApiView):
    """
    Exchange consumer key & secret for bearer token
    """

    @crossdomain(origin='*', headers=['*'])
    def post(self):
        grant_type = request.form.get('grant_type', '')

        if grant_type != 'client_credentials':
            return self.bad_request()

        if request.authorization is not None:
            key = request.authorization['username']
            secret = request.authorization['password']
            try:
                consumer = Consumer.objects.get(key=key, secret=secret)
            except DoesNotExist:
                return self.unauthorized()
            bearer_token = consumer.bearer_token
            if bearer_token.has_expired():
                bearer_token.renew()

        resp_data = {
            'token_type': 'bearer',
            'access_token': bearer_token.token,
        }
        return json_response(resp_data)
