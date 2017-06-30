from __future__ import unicode_literals

import os


def parse_boolean(value):
    if value is None:
        return None
    if value is True:
        return True
    if value == 'true':
        return True
    return False


def env(extra):
    environ = os.environ.copy()
    environ.update(extra)
    return environ
