# -*- coding: utf-8 -*-
from flask.views import MethodView, request
from flask import Response
from .util import json_response
from .models import *
from mongoengine.queryset import DoesNotExist


class ApiView(MethodView):

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

    def unsupported_media_type(self):
        return Response(status=415)


class TokenView(ApiView):
    """
    Exchange consumer key & secret for bearer token
    """

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
