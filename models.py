# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime
import random


def _generate_hash():
    return '%032x' % random.getrandbits(128)


class Consumer(Document):
    name = StringField(max_length=30, required=True)
    description = StringField(max_length=150)
    key = StringField(default=_generate_hash, required=True)
    secret = StringField(default=_generate_hash, required=True)
    created_at = DateTimeField(default=datetime.now, required=True)

    def __unicode__(self):
        return self.name


class BearerToken(Document):
    consumer = ReferenceField(Consumer, required=True)
    token = StringField(default=_generate_hash, required=True)
    expires_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now, required=True)

    def __unicode__(self):
        return self.token
