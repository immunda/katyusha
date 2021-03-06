# -*- coding: utf-8 -*-


class ModelInstanceError(Exception):

    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors

    def __str__(self):
        return repr(self.value)

    def errors(self):
        return self.errors

    def message(self):
        return self.__str__()


class InvalidDataError(Exception):

    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors

    def __str__(self):
        return repr(self.value)

    def errors(self):
        return self.errors

    def message(self):
        return self.__str__()