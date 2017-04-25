#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os
import sys
import argparse
import collections
import datetime
import tempfile

try:
    # Python 2
    from ConfigParser import RawConfigParser
except ImportError:  # pragma: no cover
    from configparser import RawConfigParser

from subprocess import Popen, CalledProcessError


CompletedProcess = collections.namedtuple('CompletedProcess', ('args', 'returncode', 'stdout', 'stderr'))


def run(cmd, *args, **kwargs):
    # Backported from Python 3.5.
    check = kwargs.pop('check', False)
    process = Popen(cmd, *args, **kwargs)
    try:
        stdout, stderr = process.communicate()
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise CalledProcessError(retcode, cmd, output=stdout)
    return CompletedProcess(cmd, retcode, stdout, stderr)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('config', help="path to the Qvarn's configuration file")
    parser.add_argument('url', nargs='?', default='https://127.0.0.1:9443', help="Qvarn server url")
    parser.add_argument('--snapshot', action='store_true', help="preserve test data")
    parser.add_argument('-h', '--help', action='store_true', help="show help")
    args, argv = parser.parse_known_args()

    if args.help:
        parser.print_help()
        print()
        print()
        return run(['yarn', '--help']).returncode

    config = RawConfigParser()
    config.read(args.config)
    log = config.get('main', 'log')

    # Add virtualenv bin directory to PATH if needed.
    if os.path.dirname(sys.executable) not in os.environ['PATH'].split(':'):
        os.environ['PATH'] = os.path.dirname(sys.executable) + ':' + os.environ['PATH']

    # Remember when tests where started.
    started = datetime.datetime.utcnow()
    timestamp = started.isoformat()

    # Create snapshot directory if needed.
    if args.snapshot:
        tmpdir = tempfile.mkdtemp(prefix='qvarn-test-snapshot-' + started.strftime('%y%m%d-%H%M%S-'))
        argv += ['--snapshot', '--tempdir', tmpdir]

    # Run tests.
    command = ['bash', 'test-api', args.url] + argv
    result = run(command, cwd='docs/qvarn-api-doc')

    # Show log content if tests failed.
    if log and result.returncode != 0:
        run(['python', '../readlogs.py', args.config, '--since', timestamp], check=True)

    # Let user know snapshot directory.
    if args.snapshot:
        print('Snapshot dir:', tmpdir)

    return result.returncode


if __name__ == "__main__":
    exit(main())
