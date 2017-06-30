from __future__ import unicode_literals

import jwt


def test_gluu_authorize(app):
    state = '2ab4b14c-ce94-4812-8eff-9e17b20aebed'
    resp = app.get('/oxauth/seam/resource/restv1/oxauth/authorize', {
        'ui_locales': 'en',
        'client_id': '%40%212027.861B.4505.5885%210001%21200B.B5FE%210008%2175E2.AF79',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8080/api/authentication/login-complete',
        'state': state,
        'scope': 'scope1 scope2 scope3',
    })
    assert resp.status == '302 Temporary'
    assert resp.headers['Location'] == 'http://localhost:8080/api/authentication/login-complete?state=' + state + '&code='


def test_gluu_auth_token(app, appconfig):
    resp = app.post('/auth/token', {
        'grant_type': "authorization_code",
        'code': '',
        'redirect_uri': 'http://localhost:8080/api/authentication/login-complete',
    })
    assert set(resp.json.keys()) == {
        'access_token',
        'id_token',
        'refresh_token',
    }

    access_token = jwt.decode(resp.json['access_token'], verify=False)
    assert access_token['scope'] == 'scope1 scope2'


def test_gluu_user_info(app):
    resp = app.post('/oxauth/seam/resource/restv1/oxauth/userinfo', {
        'grant_type': "authorization_code",
        'code': '',
        'redirect_uri': 'http://localhost:8080/api/authentication/login-complete',
    })
    assert resp.json == {
        'sub': 'qvarn-person-id',
        'inum': 'gluu-user-id',
    }


def test_gluu_create_user(app, db):
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
