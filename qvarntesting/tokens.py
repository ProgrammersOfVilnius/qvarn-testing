from __future__ import unicode_literals

import time

import jwt


PRIVATE_TEST_KEY = '''-----BEGIN RSA PRIVATE KEY-----
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


def get_jwt_token(params=None):
    now = time.time()
    payload = {
        'oxValidationURI': 'https://gluu.example.com/oxauth/opiframe',
        'oxOpenIDConnectVersion': 'openidconnect-1.0',
        'c_hash': 'dSxmNqq0uc7rT-c0qgr276hH-yUaW9HMaKY-2xyBM90',
        'aud': '@!1E2D.4C48.2272.F616!0001!CC3B.680A!0008!C2A9.C9A2',
        'sub': 'useridhash',
        'iss': 'https://gluu.example.com',
        'exp': now + 3600,
        'iat': now - 120,
        'alg': 'RS512',
        'auth_time': now - 60,
    }

    if params:
        payload.update(params)

    # jwt.encode returns bytes but we want str to be able encode it in json later
    return jwt.encode(payload, PRIVATE_TEST_KEY, algorithm='RS512').decode('utf-8')


def get_gluu_jwt_token(lifetime=3600):
    now = time.time()
    payload = {
        'iat': now,
        'exp': now + lifetime,
    }
    # jwt.encode returns bytes but we want str to be able encode it in json later
    return jwt.encode(payload, 'shared secret key').decode('utf-8')
