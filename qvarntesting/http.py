from __future__ import unicode_literals
from __future__ import absolute_import

import json


def json_response(response):
    return [json.dumps(response).encode('utf-8')]
