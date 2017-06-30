from __future__ import unicode_literals

import os
import json

from six.moves.configparser import ConfigParser
from six.moves.urllib.parse import urlencode

from qvarntesting import services
from qvarntesting.http import json_response
from qvarntesting.tokens import get_jwt_token


def auth_token(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])

    config = ConfigParser()
    config.read(os.environ['APP_CONFIG'])
    scopes = (config.get('qvarn', 'scope') or '').replace(',', ' ').split()

    return json_response({
        'access_token': get_jwt_token({
            'scope': ' '.join(scopes),
        }),
        'id_token': get_jwt_token(),
        'refresh_token': get_jwt_token(),
    })


def authorize(request, start_response):
    start_response(b'302 Temporary', [
        ('Location', request.GET['redirect_uri'] + '?' + urlencode({
            'state': request.GET.get('state'),
            'code': '',
        })),
    ])
    return []


def user_info(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])
    return json_response({
        'sub': 'qvarn-person-id',
        'inum': 'gluu-user-id',
    })


def rsrc_pr(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])
    return json_response({
        'ticket': '',
    })


def perm(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])
    return json_response({
        'rpt': '',
    })


def get_user(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])
    return json_response(services.get_gluu_user(1))


def create_user(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])

    with services.database() as db:
        user_id = db['gluu_user'].insert({
            'data': json.dumps(request.json),
        })

    return json_response(services.get_gluu_user(user_id))


def get_users(request, start_response):
    start_response(b'200 OK', [('Content-type', 'application/json')])

    with services.database() as db:
        users = [
            services.get_gluu_user(row['id'])
            for row in db['gluu_user'].all()
        ]

    return json_response(users)
