#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)
