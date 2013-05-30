# -*- coding: utf-8 -*-


class Adaptor(object):

    def __init__(self, model, child=False, readonly=False, *args, **kwargs):
        self.model = model
        self.child = child
        self.readonly = readonly

    def generate_error_message(self, errors):
        model_name = self.model._class_name.lower()
        if self.child:
            error_dict = {}
            for key, value in errors.items():
                error_dict['%s.%s' % (model_name, key)] = value
        else:
            error_dict = errors

        if self.readonly:
            message = "Failure to find '%s' with provided data" % model_name
        else:
            message = "Failure to validate data"

        content = {
            'message': message,
            'errors': error_dict,
        }
        return content

    def munge(self, data):
        munged_data = data

        for field in data:
            method_name = 'munge_%s' % field
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                munged_data[field] = method(data[field])
        return munged_data

    @property
    def readable_fields(self):
        return []

    @property
    def writable_fields(self):
        return []
