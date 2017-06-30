from __future__ import unicode_literals

import os


def set_up_gluu_db(basedir):
    vardir = os.path.join(basedir, 'var')

    if not os.path.exists(vardir):
        os.makedirs(vardir)
