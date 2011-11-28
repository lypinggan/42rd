# -*- coding: utf-8 -*-
'''
使用方法：
from iapp.utils.jsonify import jsonify

    @app.route('/')
    @jsonify
    def index():
        return {'foo': 'bar', 'baz': [1,2,3]}

'''

try:
    from json import dumps
except ImportError:
    from simplejson import dumps

from flask import Response

def jsonify(f):
    def inner(*args, **kwargs):
        return Response(dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner

