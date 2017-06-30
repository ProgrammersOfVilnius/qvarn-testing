from __future__ import unicode_literals
from __future__ import absolute_import

import os
import logging

import pkg_resources as pres

logger = logging.getLogger(__name__)


def template(configdir, filename, context):
    content = pres.resource_string('qvarntesting', 'config/%s' % filename)
    path = os.path.join(configdir, filename)
    logger.info('creating %s', path)
    with open(path, 'w') as f:
        f.write(content.format(**context))
    return path


def create_config_files(basedir):
    configdir = os.path.join(basedir, 'etc')

    if not os.path.exists(configdir):
        os.makedirs(configdir)

    template(configdir, 'haproxy.cfg', {
        'basedir': basedir,
    })

    template(configdir, 'qvarn.conf', {
        'dbuser': os.environ['USER'],
        'basedir': basedir,
    })


def set_up_configs(basedir):
    if os.path.exists(basedir):
        logger.info('configs: %s', os.path.join(basedir, 'etc'))
    else:
        create_config_files(basedir)
