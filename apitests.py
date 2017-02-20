#!/usr/bin/env python3

import os
import sys

from subprocess import run


def main():
    os.chdir('docs/qvarn-api-doc')
    venv = sys.argv[1]
    environ = dict(
        os.environ,
        PATH=os.path.join(venv, 'bin') + ':' + os.environ['PATH'],
    )
    command = ['/bin/bash', 'test-api'] + sys.argv[2:]
    return run(command, env=environ).returncode


if __name__ == "__main__":
    exit(main())
