from __future__ import unicode_literals
from __future__ import absolute_import

import os


def set_up_gluu_db(basedir):
    vardir = os.path.join(basedir, 'var')

    if not os.path.exists(vardir):
        os.makedirs(vardir)
