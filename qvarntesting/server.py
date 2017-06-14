#!/usr/bin/env python

import sys
import json
import time
import jwt
import argparse

try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl  # noqa

import qvarn


private_test_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApbW6bK3hmCGyBAM0RHd7nZMn+/NHOzsd4jJoOcSeJIk9SPnT
m/l/2ycUEEuqyt5hoyABjofZJV8S3RHk/fCaHeb0mvKokhoTXQQKTHOWvUyKKtqV
6YGmwwKD6WEyPSJbEtBVElr5j/YTYco/D0sIrbhUMVSpCIQT/I1ytGOlnLfqHM20
HSQusgtRjkUWkaDCBFHebY5C7CpnHNyd5ApeQC2MiZDSpi67GraMJ4ttbimWRUYA
dsYU11lLlPdpXgwiTeDz8pAsYSajXQVX7WBWnWC11JYMBXcu480eavDNdBTHt++Z
lcWYutGoAK5XTWhRg46jRVOmmHumj3yNh9W+xwIDAQABAoIBAQCX62KNTmB7a7Db
cuCRQIVI8md+2gtc5xa/kHzzMSnWzycrZza0UWoBTfNb+TMMqBIVTjt/I1ZVp7MQ
j95DXTi930YzY/Jdd6B270RN0M7Kn4gwP5OerylmsUCkTmKTn5KlTfAgUt1nOS+N
wLBNYfoD4fD2BOqvDv+P01HsxUpIwO3xEKp6TvkumnbXgDjgyVrGFoYCgSu/7xuX
KnqSRz2KvvukAP0ZkLrT69oCUodv4Ya336yjEGgD7YFlvkHjEl97kwr5ziNuoCer
04iLsKRV2Lj+4oy4HKFdxaGAiENLR4VNrhZDINMBKCe/vgpDXfN6jUCuxdb7ndN9
2l+9eZxpAoGBANVtHQ2fNs/jyaWdvh42BJycZbmcC5xZ78ipSzDZ6IqLzTd85zeW
0a4Roxv4viZncp/WuV1hYigE3uv+qpTLSEzdANfY3SXUUv0q+undcO8huaFNdpgF
DpkQD/uwFxkYdNiD/FWCP9BRUSQM4k468S38OEe93PX1QiTmMcQBfOvdAoGBAMbD
6ufUucu9CB+t6OcDICAboLXvmWKTzUOUraENRwLxn2cdfWmbbKBqxK6xHpusWjYp
qwS4Y+hfXM1flbIGirYjIqkjCdeSY4naVyOo4QqCyPIK9RXwHjysSLi/Kc7LL3KP
yzcEHYIm7UAxlm9VTIgefUhvwA2SVfNxPOykiYzzAoGBAJMS0BSVBQaZqFmyrFLR
UrhBpnATsoSaDX0v/Jq7b14aHN8B+av7CJ91k/swnIiGfRzcsXxCIYwGX0AtjItg
0n/1RCF6Vls9R7sipSoH6U1A5lTbtr/nrDmaMgl1PVWT3uFdgsPCMAt0HgBDyKe0
QoM37eiyU9RCoMQgxWaWx+kZAoGBAMavuxYo/9yYRhGcv06FQky2MU0Mh/ARPMNM
UM/HvO9FZokl4mJ5ufkVISxa4vTMMZUoy8o5I615/gNRhArkHS56KsCVxNXXgGah
ei+sNeBS4dmJeHqIf0E5GqyKcplDZFeJQ6LoGzMqBEkCCJWb15fNmoCZLIqkeASU
ckk/JDxfAoGAHUjRwU36XhH4wKrGd71avRc1nx6OGVuwzyiiZEEaaLPrXg8gJBaR
ec1V6k23+H/CRrzMFGZCIbMNQaxhPxfCaBINHygcZQ4jsIepFxmcDV++Fi/jMHMf
cImjZ9dxwWFeouQhOHalSyCiWWYgHSWw3r4jj/L/h2VjchzMOvJQt6A=
-----END RSA PRIVATE KEY-----'''


def get_post_data(environ):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        content_length = 0
    body = environ['wsgi.input'].read(content_length)
    return dict(parse_qsl(body.decode('utf-8')))


def get_jwt_token(scope):
    now = time.time()
    payload = {
        'oxValidationURI': u'https://gluu.example.com/oxauth/opiframe',
        'oxOpenIDConnectVersion': u'openidconnect-1.0',
        'c_hash': u'dSxmNqq0uc7rT-c0qgr276hH-yUaW9HMaKY-2xyBM90',
        'aud': u'@!1E2D.4C48.2272.F616!0001!CC3B.680A!0008!C2A9.C9A2',
        'sub': u'useridhash',
        'iss': u'https://gluu.example.com',
        'exp': now + 3600,
        'auth_time': now - 60,
        'iat': now - 120,
        'scope': scope,
    }

    # jwt.encode returns bytes but we want str to be able encode it in json later
    return jwt.encode(payload, private_test_key, algorithm='RS512').decode('utf-8')


def auth_token(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/json')])
    post = get_post_data(environ)
    return json.dumps({
        'scope': post['scope'],
        'access_token': get_jwt_token(post['scope']),
        'expires_in': 300,
    }).encode('utf-8')


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


def application(environ, start_response):
    path = environ.get('PATH_INFO', '')

    if path == '/auth/token':
        return auth_token(environ, start_response)
    else:
        return qvarnapp(environ, start_response)


parser = argparse.ArgumentParser()
parser.add_argument('specdir', help="directory containging resource type definitions")
args, argv = parser.parse_known_args()
argparse._sys.argv = [sys.argv[0]] + argv

app = qvarn.BackendApplication()

resource = setup_version_resource(app)
app.add_routes([resource])

qvarnapp = app.prepare_for_uwsgi(args.specdir)
