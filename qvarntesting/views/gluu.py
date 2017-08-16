from __future__ import unicode_literals
from __future__ import absolute_import

import os
import jwt
import json
import base64
import time

from six.moves.configparser import ConfigParser
from six.moves.urllib.parse import urlencode

from qvarntesting import services
from qvarntesting.http import json_response
from qvarntesting.tokens import get_jwt_token
from qvarntesting.templating import render


def auth_token(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])

    method, value = request.authorization
    if method == 'Basic':
        clientid, secret = base64.b64decode(value).split(':', 1)
    else:
        raise Exception("%s authentication method is not supported." % method)

    if request.POST['grant_type'] == 'authorization_code':
        if os.environ.get('APP_CONFIG'):
            config = ConfigParser()
            config.read(os.environ['APP_CONFIG'])
            scopes = (config.get('qvarn', 'scope') or '').replace(',', ' ').split()
        else:
            scopes = []

        user = services.get_gluu_user(int(request.POST['code']))

        return json_response({
            'access_token': get_jwt_token({
                'scope': ' '.join(scopes),
                'aud': clientid,
                'sub': request.POST['code'],
                'c_hash': 'c-hash',
            }),
            'id_token': get_jwt_token({
                'scope': ' '.join(scopes),
                'aud': clientid,
                'sub': request.POST['code'],
                'inum': request.POST['code'],
                'at_hash': 'at-hash',
                'email': next((x['value'] for x in user['emails'] if x['primary'] == 'true'), ''),
                'family_name': user.get('name', {}).get('familyName'),
                'given_name': user.get('name', {}).get('givenName'),
                'user_name': user.get('userName', ''),
                'name': user.get('displayName', ''),
            }),
            'refresh_token': 'refresh-token',
        })

    else:
        now = time.time()
        return json_response({
            'access_token': get_jwt_token({
                'aud': clientid,
                'sub': clientid,
                'scope': request.POST['scope'],

            }),
            'expires_in': now + 3600,
            'scope': request.POST['scope'],
            'token_type': 'bearer',
        })


def authorize(request, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])

    users = []
    redirect_url = request.GET['redirect_uri']
    with services.database() as db:
        for row in db['gluu_user'].all():
            user = services.get_gluu_user(row['id'])
            user['redirect_url'] = redirect_url + '?' + urlencode({
                'state': request.GET.get('state'),
                'code': user['id'],
            })
            users.append(user)

    return render('authorize.html', {
        'users': users,
    })


def user_info(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])

    method, value = request.authorization
    if method == 'Bearer':
        token = jwt.decode(value, verify=False)
    else:
        raise Exception("%s authentication method is not supported." % method)

    user = services.get_gluu_user(int(token['sub']))

    return json_response({
        'sub': token['sub'],
        'inum': token['sub'],
        'email': next((x['value'] for x in user['emails'] if x['primary'] == 'true'), ''),
        'family_name': user.get('name', {}).get('familyName'),
        'given_name': user.get('name', {}).get('givenName'),
        'user_name': user.get('userName', ''),
        'name': user.get('displayName', ''),
    })


def rsrc_pr(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    return json_response({
        'ticket': 'rsrc-pr-ticket',
    })


def perm(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    return json_response({
        'rpt': 'rtp-perm',
    })


def get_user(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])

    _, userid = request.path.rsplit('/', 1)
    user = services.get_gluu_user(int(userid))

    return json_response(user)


def create_user(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])

    with services.database() as db:
        user_id = db['gluu_user'].insert({
            'data': json.dumps(request.json),
        })

    return json_response(services.get_gluu_user(user_id))


def get_users(request, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])

    with services.database() as db:
        users = [
            services.get_gluu_user(row['id'])
            for row in db['gluu_user'].all()
        ]

    return json_response(users)
