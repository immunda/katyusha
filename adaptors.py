# -*- coding: utf-8 -*-


class Adaptor(object):

    def __init__(self, model, child=False, readonly=False):
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

    @property
    def readable_fields(self):
        return []

    @property
    def writable_fields(self):
        return []
