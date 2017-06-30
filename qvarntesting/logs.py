from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import logging.config


def configure_logging(config):
    logging.config.dictConfig(config)
    for logger in map(logging.getLogger, config['loggers'].keys()):
        logger.disabled = 0


def set_up_logging():
    configure_logging({
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)7s %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'stderr': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'qvarntesting': {
                'level': 'DEBUG',
                'handlers': ['stderr'],
            },
        },
        'version': 1,
    })
