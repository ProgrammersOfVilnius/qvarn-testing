from __future__ import unicode_literals

from qvarntesting.views import gluu
from qvarntesting.views import qvarn


def find_handler(request):
    if request.path == '/auth/token' and 'grant_type' in request.params:
        return gluu.auth_token

    elif request.path == '/auth/token':
        return qvarn.auth_token

    elif request.path == '/oxauth/seam/resource/restv1/oxauth/authorize':
        return gluu.authorize

    elif request.path == '/oxauth/seam/resource/restv1/oxauth/token':
        return gluu.auth_token

    elif request.path == '/oxauth/seam/resource/restv1/oxauth/userinfo':
        return gluu.user_info

    elif request.path == '/oxauth/seam/resource/restv1/host/rsrc_pr':
        return gluu.rsrc_pr

    elif request.path == '/oxauth/seam/resource/restv1/requester/perm':
        return gluu.perm

    elif request.method == 'GET' and request.path == '/identity/seam/resource/restv1/scim/v1/Users':
        return gluu.get_users

    elif request.method == 'GET' and request.path == '/identity/seam/resource/restv1/scim/v2/Users':
        return gluu.get_users

    elif request.method == 'GET' and request.path.startswith('/identity/seam/resource/restv1/scim/v2/Users/'):
        return gluu.get_user

    elif request.method == 'POST' and request.path == '/identity/seam/resource/restv1/scim/v1/Users':
        return gluu.create_user
