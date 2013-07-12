# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime, timedelta
import random
from base64 import b64encode


def _generate_hash():
    return '%032x' % random.getrandbits(128)


def _the_future():
    return datetime.now() + timedelta(days=180)


class BearerToken(Document):
    token = StringField(default=_generate_hash, unique=True, required=True)
    expires_at = DateTimeField(default=_the_future)
    created_at = DateTimeField(default=datetime.now, required=True)
    renewed_at = DateTimeField(default=datetime.now, required=True)

    def __unicode__(self):
        return self.token

    @property
    def b64_token(self):
        return b64encode(self.token)

    def has_expired(self):
        if self.expires_at is not None and datetime.now() >= self.expires_at:
            return True
        return False

    def renew(self):
        self.renewed_at = datetime.now()
        self.expires_at = _the_future()
        self.token = _generate_hash()
        self.save()


class Consumer(Document):
    name = StringField(max_length=30, required=True)
    description = StringField(max_length=150)
    key = StringField(default=_generate_hash, unique=True, required=True)
    secret = StringField(default=_generate_hash, unique=True, required=True)
    created_at = DateTimeField(default=datetime.now, required=True)
    bearer_token = ReferenceField(BearerToken, required=True, reverse_delete_rule=NULLIFY)

    def __unicode__(self):
        return self.name