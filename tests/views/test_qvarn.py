from __future__ import unicode_literals


def test_qvarn_auth_token(app):
    resp = app.post('/auth/token', {
        'scope': 'scope1 scope2 scope3',
    })
    assert set(resp.json.keys()) == {
        'access_token',
        'expires_in',
        'scope',
    }
    assert resp.json['scope'] == 'scope1 scope2 scope3'
