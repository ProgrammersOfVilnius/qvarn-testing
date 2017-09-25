from __future__ import unicode_literals
from __future__ import absolute_import

import sys
import argparse

import qvarn

from webob import Request

from qvarntesting import compat
from qvarntesting import server
from qvarntesting.views.qvarn import setup_version_resource
from qvarntesting.qvarnlogs import StdoutSlogWriter, FileSlogWriter


parser = argparse.ArgumentParser()
parser.add_argument('specdir', help="directory containging resource type definitions")
args, argv = parser.parse_known_args()
argparse._sys.argv = [sys.argv[0]] + argv

app = qvarn.BackendApplication()

resource = setup_version_resource(app)

if qvarn.__version_info__ == (0, 81):
    app.add_resource(resource)
elif qvarn.__version_info__ > (0, 81):
    app.add_routes([resource])
else:
    raise Exception("Unsupported Qvarn version.")

qvarn_app = app.prepare_for_uwsgi(args.specdir)
if qvarn.__version_info__ > (0, 81):
    qvarn.log.add_log_writer(StdoutSlogWriter(), qvarn.FilterAllow())
    qvarn.log.add_log_writer(FileSlogWriter('/tmp/qvarn.log'), qvarn.FilterAllow())
else:
    qvarn.log.set_log_writer(StdoutSlogWriter())


def application(environ, start_response):
    request = Request(environ)
    handler = server.find_handler(request)

    if handler:
        return handler(request, compat.start_response(start_response))
    else:
        return qvarn_app(environ, start_response)
