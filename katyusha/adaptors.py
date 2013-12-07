# -*- coding: utf-8 -*-
from .exceptions import ModelInstanceError, InvalidDataError
from mongoengine.queryset import DoesNotExist
from mongoengine import ValidationError


class Adaptor(object):

    def __init__(self, model, parent=None, children=None, populate_empty_fields=False, *args, **kwargs):
        self.model = model
        self.children = children
        self.populate_empty_fields = populate_empty_fields
        if self.children is not None:
            for child_name, child_adaptor in self.children.items():
                child_adaptor.parent = self
        else:
            self.children = {}
        self.parent = parent

    def _format_errors(self, error_fields):
        model_name = self.model._class_name.lower()
        if self.parent is not None:
            error_dict = {}
            for key, value in error_fields.items():
                error_dict['%s.%s' % (model_name, key)] = value
        else:
            error_dict = error_fields

        return error_dict

    @property
    def fields(self):
        return []

    # TODO raise exception if extra data provided
    def munge(self, data):
        if data is None:
            return
        munged_data = {}

        for field in self.fields:
            if field in data:
                if self.children is not None and field in self.children:
                    munged_data[field] = self.children[field].munge(data[field])
                else:
                    method_name = 'munge_%s' % field
                    if field in data:
                        if hasattr(self, method_name):
                            method = getattr(self, method_name)
                            munged_data[field] = method(data[field])
                        elif field in data:
                            munged_data[field] = data[field]
            elif self.populate_empty_fields:
                munged_data[field] = None

        return munged_data


class ReadAdaptor(Adaptor):

    def __init__(self, model, parent=None, children=None, populate_empty_fields=True, *args, **kwargs):
        super(ReadAdaptor, self).__init__(model, parent, children, populate_empty_fields, *args, **kwargs)

    def get_model_instance(self, *args, **kwargs):
        model_name = self.model._class_name.lower()
        if kwargs == {}:
            raise InvalidDataError("Failure to find '%s' with provided data" % model_name, self._format_errors(kwargs))
        try:
            model_instance = self.model.objects.get(**kwargs)
        except DoesNotExist:
            raise ModelInstanceError("Failure to find '%s' with provided data" % model_name, self._format_errors(kwargs))
        return model_instance


class WriteAdaptor(Adaptor):

    def munge(self, data):
        unexpected_fields = {}
        for unexpected_field in set(data) - set(self.fields):
            unexpected_fields[unexpected_field] = "Field not accepted"

        if len(unexpected_fields) > 0:
            raise InvalidDataError("Invalid data provided", self._format_errors(unexpected_fields))

        return super(WriteAdaptor, self).munge(data)


    #  TODO Change this name, not a get on a write adaptor
    def get_model_instance(self, *args, **kwargs):
        model_instance = self.model()

        for child_name, child_adaptor in self.children.items():
            child_kwargs = kwargs.pop(child_name, None)
            if child_kwargs is not None:
                child_instance = child_adaptor.get_model_instance(**child_kwargs)
                setattr(model_instance, child_name, child_instance)

        for key, value in kwargs.items():
            setattr(model_instance, key, value)

        try:
            model_instance.validate()
        except ValidationError, e:
            raise ModelInstanceError("Failure to validate data", self._format_errors(e.to_dict()))
        for field in self.fields:
            model_field = model_instance._fields[field]
            if model_field.unique:
                query_dict = {field: kwargs[field]}
                if self.model.objects.filter(**query_dict).count() > 0:
                    raise ModelInstanceError("Duplicate of existing unique data provided", self._format_errors(query_dict))

        model_instance.save()
        return model_instance