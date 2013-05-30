# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Response


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
