#!/usr/bin/env python

import sys
import argparse

import qvarn


specdir = '/etc/qvarn'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="Qvarn config file")
    parser.add_argument('specdir', help="directory containging resource type definitions")
    args = parser.parse_args()

    sys.argv = ['--config', args.config, '--prepare-storage']

    app = qvarn.BackendApplication()
    app.prepare_for_uwsgi(args.specdir)


if __name__ == "__main__":
    main()
