# -*- coding: utf-8 -*-
from .exceptions import ModelInstanceException
from mongoengine.queryset import DoesNotExist
from mongoengine import ValidationError


class Adaptor(object):

    def __init__(self, model, child=False, *args, **kwargs):
        self.model = model
        self.child = child

    def _format_errors(self, error_fields):
        model_name = self.model._class_name.lower()
        if self.child:
            error_dict = {}
            for key, value in error_fields.items():
                error_dict['%s.%s' % (model_name, key)] = value
        else:
            error_dict = error_fields

        return error_dict

    def unique_error(self):
        non_unique_message = {
            'message': "Non-unique values found in .",
            'errors': error_dict,
        }

    @property
    def fields(self):
        return []

    def munge(self, data):
        munged_data = {}
        for field in self.fields:
            method_name = 'munge_%s' % field
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                munged_data[field] = method(data[field])
            elif field in data:
                munged_data[field] = data[field]
        return munged_data


class ReadAdaptor(Adaptor):

    def get_model_instance(self, *args, **kwargs):
        model_name = self.model._class_name.lower()
        try:
            model_instance = self.model.objects.get(**kwargs)
        except DoesNotExist:
            raise ModelInstanceException("Failure to find '%s' with provided data" % model_name, self._format_errors(kwargs))
        return model_instance


class WriteAdaptor(Adaptor):

    def get_model_instance(self, *args, **kwargs):
        model_instance = self.model(**kwargs)
        try:
            model_instance.validate()
        except ValidationError, e:
            raise ModelInstanceException("Failure to validate data", self._format_errors(e.to_dict()))
        for field in self.fields:
            model_field = model_instance._fields[field]
            if model_field.unique:
                query_dict = {field: kwargs[field]}
                if self.model.objects.filter(**query_dict).count() > 0:
                    raise ModelInstanceException("Duplicate of existing unique data provided", self._format_errors(query_dict))
        return model_instance
