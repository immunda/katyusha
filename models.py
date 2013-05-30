# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime
from flask import url_for


class Consumer(Document):
    name = StringField()
    description = StringField()
    key = StringField()
    secret = StringField()

    def __unicode__(self):
        return self.name


class BearerToken(Document):
    consumer = ReferenceField(Consumer)
    token = StringField()
    expires = DateTimeField()

    def __unicode__(self):
        return self.token
