#!/usr/bin/env python

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import io
import json
import argparse
import collections

from qvarntesting.qvarnlogs import format_log_line


try:
    # Python 2
    from ConfigParser import RawConfigParser
    PY2 = True
except ImportError:  # pragma: no cover
    from configparser import RawConfigParser
    PY2 = False

from glob import glob
from operator import itemgetter


def parse_log_file(path):
    with io.open(path, encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            data['_filename'] = str(path)
            yield data


def get_last_entries(paths, filter, tail=2, since=None):
    tail = collections.deque([], tail)
    since = since.replace('T', ' ') if since else None
    for path in sorted(paths, reverse=True):
        tail.append(path)
        for msg in sorted(parse_log_file(path), key=itemgetter('_timestamp'), reverse=True):
            if filter(msg):
                yield tail, msg
            if since is not None and msg['_timestamp'] < since:
                break
        else:
            continue
        break


def take(n, items):
    for i, item in enumerate(items, 1):
        if n is not None and i > n:
            break
        else:
            yield item


def has_error_status(msg):
    if msg['msg_type'] == 'error':
        return True
    if msg['msg_type'] == 'http-response' and msg['status'] >= 500:
        return True
    if '_traceback' in msg:
        return True
    return False


def has_context(msg):
    def filter(x):
        return (
            msg['_context'] == x['_context'] and
            msg['_process_id'] == x['_process_id'] and
            msg['_thread_id'] == x['_thread_id']
        )
    return filter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="path to the Qvarn logs")
    parser.add_argument('limit', nargs='?', type=int, default=None)
    parser.add_argument('--since', type=str, default=None)
    args = parser.parse_args()

    config = RawConfigParser()
    config.read(args.config)
    log = config.get('main', 'log')

    if log == 'syslog':
        print('Error: syslog is not supported by this script.')
        return 1

    paths = glob('%s-*.log' % log)
    for tail, msg in take(args.limit, get_last_entries(paths, has_error_status, since=args.since)):
        messages = list(get_last_entries(tail, has_context(msg)))
        for _, msg in reversed(messages):
            line = format_log_line(msg)
            if line:
                print(line)

    return 0


if __name__ == "__main__":
    exit(main())
