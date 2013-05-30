# -*- coding: utf-8 -*-
from .views import *
from codeclubworld import app


token_view = TokenView.as_view('token')
app.add_url_rule('/token', 'token', view_func=token_view, methods=['POST'])
