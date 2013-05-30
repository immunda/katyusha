# -*- coding: utf-8 -*-
from flask import Response
import json


def json_response(data=None, status_code=200, headers=None, skip_encoding=False):
    if skip_encoding:
        json_data = data
    else:
        json_data = json.dumps(data)

    response = Response(json_data, status_code, mimetype='application/json')

    response.headers['Access-Control-Allow-Origin'] = '*'
    if headers is not None:
        for header, value in headers:
            response.headers[header] = value

    return response
