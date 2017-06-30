from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import argparse
import logging

import pkg_resources as pres

from honcho.manager import Manager

from qvarntesting.logs import set_up_logging
from qvarntesting.configs import set_up_configs
from qvarntesting.constants import DEFAULT_BASE_DIR
from qvarntesting.database import set_up_gluu_db
from qvarntesting.utils import env

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specdir', help="directory containging resource type definitions")
    parser.add_argument('appconfig', help="app configuration file")
    parser.add_argument('-d', '--basedir', default=DEFAULT_BASE_DIR, help="path to config files and etc.")
    args = parser.parse_args()

    set_up_logging()
    set_up_configs(args.basedir)
    set_up_gluu_db(args.basedir)

    haproxy_cfg = os.path.join(args.basedir, 'etc', 'haproxy.cfg')
    qvarn_conf = os.path.join(args.basedir, 'etc', 'qvarn.conf')
    gluu_db_uri = 'sqlite:///' + os.path.abspath(os.path.join(args.basedir, 'var', 'gluu.db'))

    logger.info('gluu db: %s', gluu_db_uri)

    m = Manager()

    uwsgi = ' '.join([
        'uwsgi',
        '--http-socket 127.0.0.1:9000',
        '--wsgi-file', pres.resource_filename('qvarntesting', 'wsgi.py'),
        '--pyargv "%s --config %s"' % (args.specdir, qvarn_conf),
        '--master',
        # Default buffer-size is 4k, and I already hit that limit.
        '--buffer-size 10240',
        '--py-autoreload 1',
    ])
    logger.info(uwsgi)
    m.add_process('uwsgi', uwsgi, env=env({
        'APP_CONFIG': args.appconfig,
        'DATABASE_URL': gluu_db_uri,
    }))

    haproxy = 'haproxy -f %s -C %s -db' % (
        haproxy_cfg,
        pres.resource_filename('qvarntesting', 'config/certs'),
    )
    logger.info(haproxy)
    m.add_process('haproxy', haproxy)

    m.loop()

    return m.returncode


if __name__ == '__main__':
    sys.exit(main())
