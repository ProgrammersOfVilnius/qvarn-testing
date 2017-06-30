from __future__ import unicode_literals

import os
import textwrap
import contextlib

import pytest
import dataset

from webob import Request
from webtest import TestApp

from qvarntesting.utils import env
from qvarntesting import server
from qvarntesting import compat


def _app(environ, start_response):
    request = Request(environ)
    handler = server.find_handler(request)

    if handler:
        return handler(request, compat.start_response(start_response))
    else:
        start_response('404 Not Found', [('Content-type', 'application/json')])
        return []


@pytest.fixture()
def app():
    return TestApp(_app)


@pytest.fixture()
def db(mocker):
    # os.environ['DATABASE_URL'] = 'sqlite://'
    conn = dataset.connect('sqlite://')

    @contextlib.contextmanager
    def database():
        yield conn

    mocker.patch('qvarntesting.services.database', database)

    return conn


@pytest.fixture()
def appconfig(mocker, tmpdir):
    tmpdir.join('app.cfg').write(textwrap.dedent('''\
        [qvarn]
        scope =
          scope1,
          scope2,
    '''))
    mocker.patch.dict(os.environ, env({
        'APP_CONFIG': str(tmpdir.join('app.cfg')),
    }))
