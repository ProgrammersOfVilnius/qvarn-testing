from __future__ import unicode_literals

import json


def json_response(response):
    return [json.dumps(response).encode('utf-8')]
