#!/usr/bin/env python

import os
from subprocess import check_call


for resource_type in os.listdir('src'):
    path = os.path.join('src', resource_type)
    if os.path.isfile(path) and os.access(path, os.X_OK):
        print('prapare-db: %r' % resource_type)
        check_call([path, '--config', '../qvarn.conf', '--prepare-storage'])
