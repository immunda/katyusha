# -*- coding: utf-8 -*-
from .models import *


def is_authenticated(token):
    token = BearerToken.objects.get(token=token)
    print token
