from __future__ import unicode_literals

import jwt
import json

from six import text_type

# https://gluu.org/docs/ce/3.0.2/api-guide/openid-connect-api/


def test_auth_token_authorization_code(app, db, appconfig):
    userid = db['gluu_user'].insert({
        'data': json.dumps({
            'displayName': 'Thomas Anderson',
            'name': {'familyName': 'Anderson', 'givenName': 'Thomas'},
            'emails': [{'primary': 'true', 'value': 'admin@example.com'}],
            'userName': 'admin@example.com',
        }),
    })

    clientid = 'clientid'
    userid = text_type(userid)

    app.authorization = ('Basic', (clientid, 'secret'))
    resp = app.post('/oxauth/seam/resource/restv1/oxauth/token', {
        'grant_type': "authorization_code",
        'code': userid,
        'redirect_uri': 'http://localhost:8080/api/authentication/login-complete',
    })

    data = dict(resp.json)

    access_token = jwt.decode(data.pop('access_token'), verify=False)
    del access_token['auth_time']
    del access_token['exp']
    del access_token['iat']
    assert access_token == {
        'aud': clientid,
        'sub': userid,
        'c_hash': 'c-hash',
        'iss': 'http://127.0.0.1:9000',
        'oxOpenIDConnectVersion': 'openidconnect-1.0',
        'oxValidationURI': 'http://127.0.0.1:9000/oxauth/opiframe',
        'scope': 'scope1 scope2',
        'alg': 'RS512',
    }

    id_token = jwt.decode(data.pop('id_token'), verify=False)
    del id_token['auth_time']
    del id_token['exp']
    del id_token['iat']
    assert id_token == {
        'aud': clientid,
        'sub': userid,
        'inum': userid,
        'alg': 'RS512',
        'iss': 'http://127.0.0.1:9000',
        'at_hash': 'at-hash',
        'oxOpenIDConnectVersion': 'openidconnect-1.0',
        'oxValidationURI': 'http://127.0.0.1:9000/oxauth/opiframe',
        'email': 'admin@example.com',
        'family_name': 'Anderson',
        'given_name': 'Thomas',
        'user_name': 'admin@example.com',
        'name': 'Thomas Anderson',
        'scope': 'scope1 scope2',
    }

    assert data == {
        'refresh_token': 'refresh-token'
    }


def test_auth_token_client_credentials(app, appconfig):
    clientid = 'clientid'

    app.authorization = ('Basic', (clientid, 'secret'))
    resp = app.post('/oxauth/seam/resource/restv1/oxauth/token', {
        'grant_type': 'client_credentials',
        'scope': 'uma_protection'
    })

    data = dict(resp.json)

    access_token = jwt.decode(data.pop('access_token'), verify=False)
    del access_token['auth_time']
    del access_token['exp']
    del access_token['iat']
    assert access_token == {
        'aud': clientid,
        'sub': clientid,
        'iss': 'http://127.0.0.1:9000',
        'oxOpenIDConnectVersion': 'openidconnect-1.0',
        'oxValidationURI': 'http://127.0.0.1:9000/oxauth/opiframe',
        'scope': 'uma_protection',
        'alg': 'RS512',
    }

    del data['expires_in']
    assert data == {
        'scope': 'uma_protection',
        'token_type': 'bearer',
    }


def test_user_info(app, db):
    userid = db['gluu_user'].insert({
        'data': json.dumps({
            'displayName': 'Thomas Anderson',
            'name': {'familyName': 'Anderson', 'givenName': 'Thomas'},
            'emails': [{'primary': 'true', 'value': 'admin@example.com'}],
            'userName': 'admin@example.com',
        }),
    })

    clientid = 'clientid'
    userid = text_type(userid)

    resp = app.get('/oxauth/seam/resource/restv1/oxauth/userinfo', headers={
        'Authorization': b'Bearer ' + jwt.encode({
            'aud': clientid,
            'sub': userid,
            'c_hash': 'c-hash',
            'auth_time': 1498826466,
            'exp': 1498830069,
            'iat': 1498826469,
            'iss': 'http://127.0.0.1:9000',
            'scope': 'scope1 scope2',
            'oxValidationURI': 'http://127.0.0.1:9000/oxauth/opiframe',
            'oxOpenIDConnectVersion': 'openidconnect-1.0',
        }, 'secret'),
    })
    assert resp.json == {
        'inum': userid,
        'sub': userid,
        'email': 'admin@example.com',
        'family_name': 'Anderson',
        'given_name': 'Thomas',
        'name': 'Thomas Anderson',
        'user_name': 'admin@example.com',
    }


def test_create_user(app, db):
    user = {
        'customAttributes': [
            {'name': 'personResourceId', 'values': ['0035-7e4f42114d27f42dcfa00390827d4501-ed1cc571']},
        ],
        'displayName': 'Thomas Anderson',
        'emails': [
            {'primary': 'true', 'type': 'work', 'value': 'admin@example.com'},
        ],
        'entitlements': [],
        'externalId': '0035-7e4f42114d27f42dcfa00390827d4501-ed1cc571',
        'groups': [],
        'id': '1',
        'ims': [],
        'locale': '',
        'meta': {'created': '', 'lastModified': '', 'location': '', 'version': ''},
        'name': {
            'familyName': 'Anderson',
            'givenName': 'Thomas',
            'honorificPrefix': '',
            'honorificSuffix': '',
            'middleName': '',
        },
        'nickName': '',
        'password': 'Hidden for Privacy Reasons',
        'phoneNumbers': [],
        'photos': [],
        'profileUrl': '',
        'roles': [],
        'title': '',
        'userName': 'admin@example.com',
        'userType': '',
        'x509Certificates': [],
        'addresses': [],
    }

    resp = app.post_json('/identity/seam/resource/restv1/scim/v1/Users', {
        'customAttributes': [
            {'name': 'gluuStatus', 'values': ['active']},
            {'name': 'mail', 'values': ['admin@example.com']},
            {'name': 'personResourceId', 'values': ['0035-7e4f42114d27f42dcfa00390827d4501-ed1cc571']},
        ],
        'displayName': 'Thomas Anderson',
        'emails': [
            {'primary': True, 'type': 'work', 'value': 'admin@example.com'},
        ],
        'externalId': '0035-7e4f42114d27f42dcfa00390827d4501-ed1cc571',
        'meta': {'created': None},
        'name': {'familyName': 'Anderson', 'givenName': 'Thomas'},
        'password': 'VerySecret42',
        'schemas': ['urn:scim:schemas:core:1.0'],
        'userName': 'admin@example.com',
    })

    assert resp.json == user

    resp = app.get('/identity/seam/resource/restv1/scim/v1/Users')
    assert resp.json == [user]


def test_get_user(app, db):
    userid = db['gluu_user'].insert({
        'data': json.dumps({
            'displayName': 'Thomas Anderson',
            'name': {'familyName': 'Anderson', 'givenName': 'Thomas'},
            'emails': [{'primary': 'true', 'value': 'admin@example.com'}],
            'userName': 'admin@example.com',
        }),
    })

    userid = text_type(userid)

    resp = app.get('/identity/seam/resource/restv1/scim/v2/Users/%s' % userid)
