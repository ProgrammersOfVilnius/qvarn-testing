from __future__ import unicode_literals
from __future__ import absolute_import

import qvarn

from qvarntesting.http import json_response
from qvarntesting.tokens import get_jwt_token


def version():
    return {
        'api': {
            'version': qvarn.__version__,
        },
        'implementation': {
            'name': 'Qvarn',
            'version': qvarn.__version__,
        },
    }


def setup_version_resource(app):
    vs = qvarn.VersionedStorage()
    vs.set_resource_type('version')
    app.add_versioned_storage(vs)

    resource = qvarn.SimpleResource()
    resource.set_path(u'/version', version)
    return resource


def auth_token(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    return json_response({
        'scope': request.POST['scope'],
        'access_token': get_jwt_token({
            'aud': 'client-id',
            'sub': 'user-id',
            'scope': request.POST['scope'],
        }),
        'expires_in': 300,
    })
