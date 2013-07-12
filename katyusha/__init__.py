# -*- coding: utf-8 -*-
from .decorators import authenticate, crossdomain
from .views import TokenView
from .auth import is_authenticated
from .util import json_response


def load_routes(app):
    token_view = TokenView.as_view('token')
    app.add_url_rule('/token', 'token', view_func=token_view, methods=['POST', 'OPTIONS'])
