from __future__ import unicode_literals
from __future__ import absolute_import

import json


def test_authorize(app, db):
    db['gluu_user'].insert({
        'data': json.dumps({
            'displayName': 'Thomas Anderson',
            'name': {'familyName': 'Anderson', 'givenName': 'Thomas'},
            'emails': [{'primary': 'true', 'value': 'admin@example.com'}],
            'userName': 'admin@example.com',
        }),
    })

    state = 'state'
    resp = app.get('/oxauth/seam/resource/restv1/oxauth/authorize', {
        'ui_locales': 'en',
        'client_id': '%40%212027.861B.4505.5885%210001%21200B.B5FE%210008%2175E2.AF79',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8080/api/authentication/login-complete',
        'state': state,
        'scope': 'scope1 scope2 scope3',
    })
    assert [(x.attrib['href'], x.text) for x in resp.lxml.xpath('//ul[@id="user-list"]//a')] == [
        ('http://localhost:8080/api/authentication/login-complete?state=state&code=1', 'Thomas Anderson'),
    ]
