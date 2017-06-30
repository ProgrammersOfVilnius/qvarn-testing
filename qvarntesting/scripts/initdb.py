#!/usr/bin/env python

from __future__ import unicode_literals

import os
import sys
import argparse

import qvarn

from qvarntesting.logs import set_up_logging
from qvarntesting.configs import set_up_configs
from qvarntesting.constants import DEFAULT_BASE_DIR


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specdir', help="directory containging resource type definitions")
    parser.add_argument('-d', '--basedir', default=DEFAULT_BASE_DIR, help="path to config files and etc.")
    args = parser.parse_args()

    set_up_logging()
    set_up_configs(args.basedir)

    argparse._sys.argv = [sys.argv[0]] + [
        '--config', os.path.join(args.basedir, 'etc', 'qvarn.conf'),
        '--prepare-storage',
    ]

    app = qvarn.BackendApplication()
    app.prepare_for_uwsgi(args.specdir)


if __name__ == "__main__":
    main()
