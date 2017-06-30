from __future__ import unicode_literals

import jwt


def test_qvarn_auth_token(app):
    resp = app.post('/auth/token', {
        'scope': 'scope1 scope2 scope3',
    })

    data = dict(resp.json)
    id_token = jwt.decode(data.pop('access_token'), verify=False)
    del id_token['auth_time']
    del id_token['exp']
    del id_token['iat']
    assert id_token == {
        'aud': 'client-id',
        'sub': 'user-id',
        'alg': 'RS512',
        'iss': 'http://127.0.0.1:9000',
        'oxOpenIDConnectVersion': 'openidconnect-1.0',
        'oxValidationURI': 'http://127.0.0.1:9000/oxauth/opiframe',
        'scope': 'scope1 scope2 scope3',
    }

    del data['expires_in']
    assert data == {
        'scope': 'scope1 scope2 scope3'
    }
