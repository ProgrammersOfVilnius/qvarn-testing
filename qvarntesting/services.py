from __future__ import unicode_literals
from __future__ import absolute_import

import os
import json
import contextlib

import dataset

from qvarntesting.utils import parse_boolean


class NotFoundError(Exception):
    pass


@contextlib.contextmanager
def database():
    yield dataset.connect(os.environ['DATABASE_URL'])


def get_gluu_user(user_id):
    with database() as db:
        row = db['gluu_user'].find_one(id=user_id)

        if row is None:
            raise NotFoundError('gluu user id=%s not found.' % user_id)

        data = json.loads(row['data'])
        meta = data.get('meta', {})
        name = data.get('name', {})
        return {
            'id': str(row['id']),
            'addresses': data.get('addresses', []),
            'customAttributes': [
                x for x in data.get('customAttributes', [])
                if x.get('name') not in ('gluuStatus', 'mail')
            ],
            'displayName': data.get('displayName', ''),
            'emails': [
                {
                    'primary': 'true' if parse_boolean(x.get('primary')) else '',
                    'type': x.get('type', ''),
                    'value': x.get('value', ''),
                }
                for x in data.get('emails', [])
            ],
            'entitlements': data.get('entitlements', []),
            'externalId': data.get('externalId', ''),
            'groups': data.get('groups', []),
            'ims': data.get('ims', []),
            'locale': data.get('locale', ''),
            'meta': {
                'created': meta.get('created') or '',
                'lastModified': meta.get('lastModified', ''),
                'location': meta.get('location', ''),
                'version': meta.get('version', ''),
            },
            'name': {
                'familyName': name.get('familyName', ''),
                'givenName': name.get('givenName', ''),
                'honorificPrefix': name.get('honorificPrefix', ''),
                'honorificSuffix': name.get('honorificSuffix', ''),
                'middleName': name.get('middleName', ''),
            },
            'nickName': data.get('nickName', ''),
            'password': 'Hidden for Privacy Reasons',
            'phoneNumbers': data.get('phoneNumbers', []),
            'photos': data.get('photos', []),
            'profileUrl': data.get('profileUrl', ''),
            'roles': data.get('roles', []),
            'title': data.get('title', ''),
            'userName': data.get('userName', ''),
            'userType': data.get('userType', ''),
            'x509Certificates': data.get('x509Certificates', []),
        }
